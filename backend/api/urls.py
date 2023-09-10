from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from .views import TagViewSet, IngredientViewSet, RecipeViewSet, TokenCreateView, FoodUserView


router = routers.DefaultRouter()
router.register(r'api/tags', TagViewSet)
router.register(r'api/ingredients', IngredientViewSet)
router.register(r'api/recipes', RecipeViewSet)
router.register(r'api/users', FoodUserView)

urlpatterns = [
    path('api/auth/token/login/', TokenCreateView.as_view(), name="login"),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
