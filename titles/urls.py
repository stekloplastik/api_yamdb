from django.urls import include, path
from rest_framework.routers import DefaultRouter

from titles.views import CategoryViewSet, GenreViewSet, TitleViewSet

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet)
v1_router.register('genres', GenreViewSet, basename='comments')
v1_router.register('categories', CategoryViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
