from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.relations import SlugRelatedField
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from api_yamdb.settings import RESERVED_NAME
from reviews.models import Review, Comment, Category, Genre, Title
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        slug_field='id',
        many=False,
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
                request.method == 'POST'
                and Review.objects.filter(
                title=title,
                author=request.user).exists()
        ):
            raise ValidationError('Можно оставить только один отзыв')
        return data

    class Meta:
        fields = '__all__'
        model = Review

    def validate_score(self, value):
        if value > 10 or value < 1:
            raise serializers.ValidationError('Не коректно указанный рейтинг!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review')


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleCreateSerializer(ModelSerializer):
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'bio', 'email',
                  'role')
        extra_kwargs = {
            'password': {'required': False},
            'email': {'required': True}
        }


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, username):
        if username == RESERVED_NAME:
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        return username


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)
