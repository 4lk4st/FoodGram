from django.contrib import admin
from .models import Tag, Ingredient, Recipe, IngredientRecipe


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInline,)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass
