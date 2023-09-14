from djoser import utils
from djoser.conf import settings
from djoser.views import UserViewSet
from django.http import HttpResponse
from django.db.models import Sum
from rest_framework import generics, status, viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from users.models import FoodUser, Subscription
from recipes.models import (Tag, Ingredient, Recipe, FavoriteRecipe,
                            ShoppingCartRecipes, IngredientRecipe)
from api.paginators import FoodPageLimitPaginator

from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeWriteSerializer,
                          ShortRecipeSerializer, SubsciptionReadSerializer)


class TokenCreateView(utils.ActionViewMixin, generics.GenericAPIView):
    """
    Переписали djoser-овский вью-класс для отображения корректного статус-кода
    """

    serializer_class = settings.SERIALIZERS.token_create
    permission_classes = settings.PERMISSIONS.token_create
    pagination_class = FoodPageLimitPaginator

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data,
            status=status.HTTP_201_CREATED
        )


class FoodUserView(UserViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        recipes_limit = int(self.request.query_params.get('recipes_limit'))

        queryset = self.paginate_queryset(
            FoodUser.objects.filter(subscription__user=self.request.user))
        serializer = SubsciptionReadSerializer(
            queryset,
            context={'recipes_limit': recipes_limit},
            many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, **kwargs):
        subscription = get_object_or_404(FoodUser, id=kwargs['id'])

        if request.method == 'POST':
            Subscription.objects.create(
                user=request.user,
                subscription=subscription
            )
            return Response(
                SubsciptionReadSerializer(subscription).data,
                status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            Subscription.objects.get(
                user=request.user,
                subscription=subscription
            ).delete()
            return Response({'detail': 'Успешная отписка'},
                            status=status.HTTP_204_NO_CONTENT)


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
    search_fields = ('^name', )
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт для get, post, get_id, patch, del запросов по рецептам.
    """
    queryset = Recipe.objects.all()
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        author = get_object_or_404(FoodUser, id=self.request.user.id)
        serializer.save(author=author)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def get_queryset(self):
        queryset = Recipe.objects.prefetch_related(
            'recipe_ingredient__ingredient', 'tags'
        ).all()

        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()

        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author=author)

        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited:
            queryset = queryset.filter(
                recipe_in_favorite__user=self.request.user)

        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        if is_in_shopping_cart:
            queryset = queryset.filter(
                recipe_in_cart__user=self.request.user)

        return queryset

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'POST':
            FavoriteRecipe.objects.create(
                user=request.user,
                recipe=recipe
            )
            return Response(ShortRecipeSerializer(recipe).data,
                            status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            FavoriteRecipe.objects.get(
                user=request.user,
                recipe=recipe
            ).delete()
            return Response({'detail': 'Рецепт успешно удален из избранного'},
                            status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'POST':
            ShoppingCartRecipes.objects.create(
                user=request.user,
                recipe=recipe
            )
            return Response(ShortRecipeSerializer(recipe).data,
                            status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            ShoppingCartRecipes.objects.get(
                user=request.user,
                recipe=recipe
            ).delete()
            return Response(
                {'detail': 'Рецепт успешно удален из списка покупок'},
                status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        shopping_list = ['Ваш список покупок:', '\n-------------------']

        for obj in (IngredientRecipe.objects.filter(
            recipe__recipe_in_cart__user=request.user)
            .values('ingredient').annotate(Sum('amount'))
            .values_list('ingredient__name',
                         'ingredient__measurement_unit',
                         'amount__sum')):
            shopping_list.append(f'\n{obj[0]} ({obj[1]}) - {obj[2]}')
        shopping_list.append('\n-------------------\nПриятных покупок!')

        return HttpResponse(
            shopping_list,
            headers={
                "Content-Type": "text/plain",
                "Content-Disposition": 'attachment; filename="sh_list.txt"'}
        )
