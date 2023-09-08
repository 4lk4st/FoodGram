from rest_framework import serializers

from .models import FoodUser, Subscription

class FoodUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = FoodUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        if not self.context['request'].user.is_anonymous:
            return Subscription.objects.filter(
                user = self.context['request'].user,
                subscription = obj
            ).exists()
        return False
