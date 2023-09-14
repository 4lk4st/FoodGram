from django.contrib import admin
from recipes.models import (Tag, Ingredient, Recipe, IngredientRecipe,
                            FavoriteRecipe, ShoppingCartRecipes)
from users.models import FoodUser, Subscription


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


class FavoriteRecipe(admin.TabularInline):
    model = FavoriteRecipe
    extra = 1


class ShoppingCartRecipes(admin.TabularInline):
    model = ShoppingCartRecipes
    extra = 1


class Subscription(admin.TabularInline):
    model = Subscription
    extra = 1
    fk_name = "subscription"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'author',
        'in_favorites'
    )
    list_filter = ('name', 'author', 'tags')
    inlines = (IngredientRecipeInline,)

    @admin.display(description='Число добавлений в избранное')
    def in_favorites(self, obj):
        return obj.recipe_in_favorite.count()


@admin.register(FoodUser)
class FoodUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'pk',
        'email',
        'first_name',
        'last_name'
    )
    list_filter = ('username', 'email')
    inlines = (FavoriteRecipe, Subscription, ShoppingCartRecipes)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)


admin.site.register(Tag)
