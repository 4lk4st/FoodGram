import webcolors
import base64
from rest_framework import serializers
from django.core.files.base import ContentFile

from users.models import FoodUser, Subscription
from recipes.models import (Tag, Ingredient, Recipe,
                            IngredientRecipe, FavoriteRecipe,
                            ShoppingCartRecipes)


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


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
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user

        if not user.is_anonymous or not user == obj:
            return Subscription.objects.filter(
                user=user.id,
                subscription=obj
            ).exists()
        return False


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Ingredient.
    Применяется для отображения информации об ингредиенте.
    """
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Tag.
    """
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientRecipeReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода информации из модели IngredientRecipe.
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ['id', 'name', 'measurement_unit', 'amount']


class IngredientRecipeWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ввода информации для модели IngredientRecipe.
    """
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientRecipe
        fields = ['id', 'amount']


class RecipeWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для записи в модель Recipe
    """
    image = Base64ImageField(required=True, allow_null=True)
    author = FoodUserSerializer(default=serializers.CurrentUserDefault())
    ingredients = IngredientRecipeWriteSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time']
        read_only_fields = ('author',)

    def create(self, validated_data):
        ing_amount = validated_data.pop('ingredients')
        recipe = super().create(validated_data)

        for ing in ing_amount:
            IngredientRecipe.objects.create(
                ingredient=Ingredient.objects.get(pk=ing['ingredient'].id),
                recipe=recipe,
                amount=ing['amount'])
        return recipe

    def to_representation(self, instance):
        return RecipeReadSerializer(instance=instance,
                                    context=self.context).data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)

        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.set([])

            lst = []
            for tag in tags_data:
                lst.append(tag)
            instance.tags.set(lst)

        if 'ingredients' in validated_data:
            ing_amount = validated_data.pop('ingredients')
            instance.ingredients.set([])

            for ing in ing_amount:
                IngredientRecipe.objects.create(
                    ingredient=Ingredient.objects.get(pk=ing['ingredient'].id),
                    recipe=instance,
                    amount=ing['amount'])

        instance.save()
        return instance


class RecipeReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения записей модели Recipe
    """
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    author = FoodUserSerializer(default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time']
        read_only_fields = ('author',)

    def get_ingredients(self, obj):
        return IngredientRecipeReadSerializer(
            instance=obj.recipe_ingredient.all(),
            many=True
        ).data

    def get_is_favorited(self, obj):
        return FavoriteRecipe.objects.filter(
            user=self.context['request'].user.id,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingCartRecipes.objects.filter(
            user=self.context['request'].user.id,
            recipe=obj
        ).exists()


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ("__all__",)


class SubsciptionReadSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = FoodUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ("__all__",)

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        if self.context.get('recipes_limit'):
            recipes = obj.recipes.all()[0:self.context.get('recipes_limit')]
        else:
            recipes = obj.recipes.all()
        return ShortRecipeSerializer(recipes, many=True, read_only=True).data
