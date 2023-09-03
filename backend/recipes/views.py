from rest_framework import viewsets, permissions, filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from users.models import FoodUser
from users.paginators import FoodPageLimitPaginator
from .models import Tag, Ingredient, Recipe
from .serializers import TagSerializer, IngredientSerializer, RecipeReadSerializer, RecipeWriteSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API эндпоинт для просмотра списка тегов или тега по id
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API эндпоинт для просмотра списка ингредиентов или тега по ингредиенту
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт для get, post, get_id, patch, del запросов по рецептам.
    """
    queryset = Recipe.objects.all()
    permission_classes = [permissions.AllowAny]
    pagination_class = FoodPageLimitPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author', 'tags__slug')

    def perform_create(self, serializer):
        author = get_object_or_404(FoodUser, id=self.request.user.id)
        serializer.save(author=author)
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeWriteSerializer
    
    #для отладки
    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request, *args, **kwargs)
        return result

    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            'recipe_ingredient__ingredient', 'tags'
        ).all()
        return recipes
