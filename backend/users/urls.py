from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from users.views import TokenCreateView, SubscriptionsViewSet


urlpatterns = [
    path('api/auth/token/login/', TokenCreateView.as_view(), name="login"),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/users/subscriptions/', SubscriptionsViewSet.as_view({'get': 'list'}), name="subscription"),
    path('api/', include('djoser.urls')),
]
