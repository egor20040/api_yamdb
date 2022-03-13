from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (ReviewViewSet,
                       CommentViewSet,
                       CategoryViewSet,
                       GenreViewSet,
                       TitleViewSet,
                       UserViewSet,
                       get_token,
                       get_confirmation_code,
                       )

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

v1_router.register('categories', CategoryViewSet, basename='Category')
v1_router.register('genres', GenreViewSet, basename='Genre')
v1_router.register('titles', TitleViewSet, basename='Title')
v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', get_confirmation_code),
    path('v1/auth/token/', get_token),
    path('v1/', include(v1_router.urls)),
]
