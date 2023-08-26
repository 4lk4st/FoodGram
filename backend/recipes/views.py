from rest_framework import viewsets, permissions, filters

from .models import Tag, Ingredient
from .serializers import TagSerializer, IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API эндпоинт для просмотра списка тегов или тега по id
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API эндпоинт для просмотра списка ингредиентов или тега по ингредиенту
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    pagination_class = None
