from rest_framework import serializers

from .models import FoodUser

class FoodUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
