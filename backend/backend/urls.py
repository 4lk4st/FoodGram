from django.contrib import admin
from django.urls import path, include

from users import views

urlpatterns = [
    path('api/auth/token/login/', views.TokenCreateView.as_view(), name="login"),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('djoser.urls')),
    path('admin/', admin.site.urls),
]
