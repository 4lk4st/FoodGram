from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from djoser import utils
from djoser.conf import settings
from djoser.views import UserViewSet

from users.paginators import FoodPageLimitPaginator
from .models import Subscription, FoodUser
from .serializers import SubsciptionReadSerializer, SubsciptionWriteSerializer

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
            data=token_serializer_class(token).data, status=status.HTTP_201_CREATED
        )


class FoodUserView(UserViewSet):
       
    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        queryset = self.paginate_queryset(
            FoodUser.objects.filter(subscription__user=self.request.user))
        serializer = SubsciptionReadSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, **kwargs):
        subscription = get_object_or_404(FoodUser, id=kwargs['id'])
        
        if request.method == 'POST':       
            Subscription.objects.create(
                user = request.user,
                subscription = subscription
            )
            return Response(
                SubsciptionReadSerializer(subscription).data,
                status=status.HTTP_201_CREATED
            )
        
        if request.method == 'DELETE':
            Subscription.objects.get(
                user = request.user,
                subscription = subscription
            ).delete()
            return Response({'detail': 'Успешная отписка'},
                            status=status.HTTP_204_NO_CONTENT)
