from django.db import models
from django.core.validators import MinValueValidator

from users.models import FoodUser


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color =  models.CharField(max_length=7)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(FoodUser,
                               on_delete=models.CASCADE,
                               related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientRecipe')
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None)
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.IntegerField(
         validators=[
            MinValueValidator(1)
        ]
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-pk']

class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipe_ingredient')
    amount = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'{self.ingredient} {self.recipe}'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(FoodUser,
                             on_delete=models.CASCADE,
                             related_name='favorite_recipes')

    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipe_in_favorite')

    def __str__(self) -> str:
        return f'{self.user} prefers {self.recipe}'


class ShoppingCartRecipes(models.Model):
    user = models.ForeignKey(FoodUser,
                             on_delete=models.CASCADE,
                             related_name='shopping_cart')
    
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipe_in_cart')
    
    def __str__(self) -> str:
        return f'{self.user} put {self.recipe} in shopping cart'
