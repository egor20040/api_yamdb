from django.db.models import Avg
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import status, permissions, viewsets, filters
from django_filters.rest_framework import (DjangoFilterBackend,
                                           CharFilter,
                                           FilterSet)
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes

from api.permissions import IsAdminOrAuthorOrReadOnly
from reviews.models import Review, Category, Genre, Title
from users.models import User
from api.mixins import CustomViewSet
from api.permissions import IsAdminOrReadOnly, IsAdmin
from api_yamdb.settings import RESERVED_NAME
from api.serializers import (CategorySerializer,
                             GenreSerializer,
                             TitleSerializer,
                             ReviewSerializer,
                             CommentSerializer,
                             UserSerializer,
                             SignupSerializer,
                             TokenSerializer,
                             NotAdminSerializer, TitleCreateSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly,)

    @staticmethod
    def rating_calculation(title):
        int_rating = title.review.all().aggregate(Avg('score'))
        title.rating = int_rating['score__avg']
        title.save(update_fields=['rating'])

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        self.rating_calculation(title)
        return title.review.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        if Review.objects.filter(
                title=title, author=self.request.user
        ).exists():
            raise ValidationError('Можно оставить только один отзыв')
        serializer.save(author=self.request.user, title=title)
        self.rating_calculation(title)

    def perform_update(self, serializer):
        serializer.save()
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        self.rating_calculation(title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CustomViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class GenreViewSet(CustomViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class TitleFilter(FilterSet):
    category = CharFilter(
        field_name='category__slug',
    )
    genre = CharFilter(
        field_name='genre__slug',
    )
    name = CharFilter(
        field_name='name',
        lookup_expr='contains'
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializer
        return TitleCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

    @action(
        methods=('GET', 'PATCH'),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        url_path=RESERVED_NAME
    )
    def me(self, request):
        if not request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = NotAdminSerializer(request.user,
                                            data=request.data,
                                            partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


@api_view(('POST',))
@permission_classes((permissions.AllowAny,))
def get_confirmation_code(request):
    serializer = SignupSerializer(data=request.data)
    username = request.POST.get('username')
    email = request.POST.get('email')
    serializer.is_valid(raise_exception=True)
    if not User.objects.filter(email=email).exists():
        serializer.save()
    user = get_object_or_404(User,
                             email=email,
                             username=username, )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения YaMDb',
        f'Ваш код подтверждения: {confirmation_code}',
        DEFAULT_FROM_EMAIL,
        [f'{request.data["email"]}'],
        fail_silently=False,
    )
    return Response(serializer.data,
                    status=status.HTTP_200_OK)


@api_view(('POST',))
@permission_classes((permissions.AllowAny,))
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data['username']
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.data['confirmation_code']
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    token = AccessToken.for_user(user)
    return Response(
        {'token': str(token.access_token)}, status=status.HTTP_200_OK
    )
