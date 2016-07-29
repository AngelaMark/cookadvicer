from django.contrib import admin
from fb_cookbot.models import Ingredient, Recipe


class RecipeAdmin(admin.ModelAdmin):
    pass

class IngredientAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
