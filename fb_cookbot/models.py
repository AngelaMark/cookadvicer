from django.db import models

# Create your models here.

"""
class Ingredients(models.Model):
    name_ingredient = models.Charfield(max_length=30)


class Recipes(models.Model):
    name_rec = models.CharField(max_length=30)
    ingredients = models.ManyToManyField(Ingredients, through=IngredientInRecipe)

    def __str__(self):
        pass

class IngredientInRecipe(models.Model):
    ingredient_id = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    recipes_id = models.ForeignKey(Recipes, on_delete=models.CASCADE)

"""