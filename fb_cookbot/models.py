from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    image_url = models.URLField(blank=True)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name
