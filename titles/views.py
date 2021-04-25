from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from titles.models import Category, Genre, Title
from titles.serializers import CategorySerializer, GenreSerializer, \
    TitleSerializer


class ListCreateDestroyModelViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    A viewset that provides default `list()`, `create()`, 'destroy()' actions.
    """
    pass


class CategoryViewSet(ListCreateDestroyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'year', 'category', 'genre', ]
    pagination_class = PageNumberPagination
