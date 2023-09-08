from rest_framework import generics, status, viewsets, permissions, filters
from rest_framework.response import Response
from djoser import utils
from djoser.conf import settings

from users.paginators import FoodPageLimitPaginator
from .models import Subscription
from .serializers import SubsciptionSerializer

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


class SubscriptionsViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Subscription.objects.filter(user=request.user)
        serializer = SubsciptionSerializer(queryset, many=True)
        return Response(serializer.data)
