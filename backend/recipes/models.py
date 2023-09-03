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
    author = models.ForeignKey(
        FoodUser,
        on_delete=models.CASCADE,
        related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientRecipe')
    tags = models.ManyToManyField(Tag)
    image = models.CharField(max_length=16)
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.IntegerField(
         validators=[
            MinValueValidator(1)
        ]
    )

    def __str__(self) -> str:
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipe_ingredient')
    amount = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'{self.ingredient} {self.recipe}'
