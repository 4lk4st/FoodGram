from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from recipes.views import TagViewSet, IngredientViewSet
from users.views import TokenCreateView

router = routers.DefaultRouter()
router.register(r'api/tags', TagViewSet)
router.register(r'api/ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/auth/token/login/', TokenCreateView.as_view(), name="login"),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('djoser.urls')),
    path('admin/', admin.site.urls),
]
