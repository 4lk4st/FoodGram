from django.urls import path, include
from rest_framework import routers

from .views import (TagViewSet, IngredientViewSet,
                    RecipeViewSet, TokenCreateView, FoodUserView,
                    FavoriteViewSet, ShoppingCartViewSet)


router = routers.DefaultRouter()
router.register(r'api/tags', TagViewSet)
router.register(r'api/ingredients', IngredientViewSet)
router.register(r'api/recipes', RecipeViewSet)
router.register(r'api/users', FoodUserView)


urlpatterns = [
    path('api/auth/token/login/', TokenCreateView.as_view(), name="login"),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/recipes/<int:id>/favorite/',
         FavoriteViewSet.as_view(),
         name='favorite'),
    path('api/recipes/<int:id>/shopping_cart/',
         ShoppingCartViewSet.as_view(),
         name='shopping_cart'),
    path('', include(router.urls)),
]
