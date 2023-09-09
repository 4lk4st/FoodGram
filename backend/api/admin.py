from django.contrib import admin
from recipes.models import Tag, Ingredient, Recipe, IngredientRecipe, FavoriteRecipe
from users.models import FoodUser, Subscription


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


class FavoriteRecipe(admin.TabularInline):
    model = FavoriteRecipe
    extra = 1


class Subscription(admin.TabularInline):
    model = Subscription
    extra = 1
    fk_name = "subscription"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInline,)


@admin.register(FoodUser)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (FavoriteRecipe, Subscription)


admin.site.register(Tag)
admin.site.register(Ingredient)
