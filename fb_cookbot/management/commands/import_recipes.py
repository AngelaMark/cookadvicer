from django.core.management.base import BaseCommand
from fb_cookbot.models import Recipe, Ingredient
import requests
import json
from urllib.request import urlopen
import urllib


def get_link_image(page_url):
    try:
        page_content = urlopen(page_url).read().decode('utf8')
        if page_content.find('"og:image" content="') != -1:
            print(page_content.find('"og:image" content="'))
            return page_content.split('"og:image" content="')[1].split('"')[0]
        else:
            return ''
    except UnicodeDecodeError as e:
        print("Error :", e)
        return ''


class Command(BaseCommand):

    def handle(self, *args, **options):
        for id in range(100200, 101000):
            try:
                recevied_message = requests.get("https://webknox-recipes.p.mashape.com/recipes/%s/information" % id,
                                           headers={
                                               "X-Mashape-Key": "ItmZYXVm0TmshdVULGUTZWksY6tMp1djoIDjsnbAsyQfkMsj6y",

                                               "Accept": "application/json"
                                           }
                                           ).json()
                if not recevied_message.get("status") == 'failure':
                    try:
                        Recipe.objects.get(name=recevied_message['title'])
                        print("exist")
                    except Recipe.DoesNotExist:
                        img_url = get_link_image(recevied_message['sourceUrl'])
                        recipe, created = Recipe.objects.update_or_create(
                            name=recevied_message['title'],
                            url=recevied_message['sourceUrl'],
                            image_url=img_url
                        )
                        print('not exist')
                        print(recevied_message['id'])
                        recipe.save()

                        for ingredient in recevied_message['extendedIngredients']:
                            try:
                                ingredient_db = Ingredient.objects.get(name=ingredient['name'])
                                print("exist")
                            except Ingredient.DoesNotExist:
                                ingredient_db, created = Ingredient.objects.update_or_create(
                                    name=ingredient['name']
                                )
                            ingredient_db.save()
                            recipe.ingredients.add(ingredient_db)
            except urllib.error.HTTPError as e:
                print("Raise error ", e)