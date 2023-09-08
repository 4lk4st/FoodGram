import base64
from rest_framework import serializers
from django.core.files.base import ContentFile

from .models import FoodUser, Subscription
from recipes.models import Recipe


class Base64ImageField(serializers.ImageField):
    """
    Поле для добавления картинок рецептов
    """
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')  
            ext = format.split('/')[-1]  
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        
        return super().to_internal_value(data)


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
    

class RecipeSubscriptionSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubsciptionSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='subscription.email')
    id = serializers.ReadOnlyField(source='subscription.id')
    username = serializers.ReadOnlyField(source='subscription.username')
    first_name = serializers.ReadOnlyField(source='subscription.username')
    last_name = serializers.ReadOnlyField(source='subscription.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeSubscriptionSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return True
    
    def get_recipes_count(self, obj):
        return 1