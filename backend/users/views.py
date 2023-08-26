from rest_framework import generics, status
from rest_framework.response import Response
from djoser import utils
from djoser.conf import settings


class TokenCreateView(utils.ActionViewMixin, generics.GenericAPIView):
    """
    Переписали djoser-овский вью-класс для отображения корректного статус-кода
    """

    serializer_class = settings.SERIALIZERS.token_create
    permission_classes = settings.PERMISSIONS.token_create

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data, status=status.HTTP_201_CREATED
        )