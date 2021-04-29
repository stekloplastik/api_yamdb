from django.db.models import Avg
from rest_framework import filters, viewsets

from titles.models import Category, Genre, Title
from titles.serializers import CategorySerializer, GenreSerializer, \
    TitleReadSerializer, TitleWriteSerializer
from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly


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
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Genre.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleReadSerializer
        else:
            return TitleWriteSerializer

    permission_classes = [IsAdminOrReadOnly]
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    filterset_class = TitleFilter
