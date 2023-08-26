from django.db import models


class Tag(models.Model):
    name = models.TextField()
    color =  models.TextField()
    slug = models.SlugField()

    class Meta:
        ordering = ['name']


class Ingredient(models.Model):
    name = models.TextField()
    measurement_unit = models.TextField()
