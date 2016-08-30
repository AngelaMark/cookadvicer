import json, requests, random, re, operator
from pprint import pprint
from django.db.models import Q
from functools import reduce

from django.db.models import Q, Count
from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from fb_cookbot.models import Recipe, Ingredient
from fb_cookbot.utils import FacebookApi

VERIFY_TOKEN = "2318934571"
PAGE_ACCESS_TOKEN = "EAAD0kpLj8bEBALiqJAwI5OSn64ByZCwc44RZCjvCz76mayWM0ZCOBKjFZA1rLeZCcJ8KnnLsjomQP0VVPtg5bhToiKKx5wWmGlS3gUQxvRJ718JXURLN5OnZAbtLj1eBpYBLJCOtZCeSfWm9WJZCPV06xicwztkeCOGkZALTRHAYt1xWEfp3qafqx"

# Helper function
def post_facebook_message(fbid, recevied_message):
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()
    if 'hi' in recevied_message.lower() or 'hello' in recevied_message.lower():
        answer = 'Hi, hungry ' + str(user_details['first_name']) + ". Tell me what ingredients you have and I'll advice you some recipes."
        FacebookApi.post_message(fbid, answer)
    else:
        ingredients_list = recevied_message.replace(', ', ',').replace(' ,', ',').replace('.','').split(',')
        print(ingredients_list)
        for ingr in ingredients_list:
            ingr.strip()
            check = False
        ingredient_in = []
        for ingredient in ingredients_list:
            try:
                ingredient_in.append(Ingredient.objects.get(name=ingredient))
            except Exception:
                pass
        if len(ingredient_in) != 0:
            check = True
        if not check:
            FacebookApi.post_message(fbid, "I can't understand, please type correct ingredients")
        else:
            query = reduce(operator.or_, (Q(name__contains=item) for item in ingredients_list))
            asked_ingredients = Ingredient.objects.filter(query)
            excluded_ingredients = Ingredient.objects.exclude(query)
            recipes1 = Recipe.objects.filter(ingredients__in=asked_ingredients)
            recipes = recipes1.exclude(ingredients__in=excluded_ingredients).distinct()
            if len(recipes) == 0:
                FacebookApi.post_message(fbid, "Sorry, I can't find recipes for you")
            else:
                elem_arrays = []
                for recipe in recipes:
                    element_of_msg = \
                    {
                        "title": "Recipe title",
                        "image_url": "",
                        "subtitle": " ",
                        "buttons": [{
                            "type": "web_url",
                            "url": "",
                            "title": "Go to recipe"
                        },
                        {
                            "type": "postback",
                            "title": "Start Chatting",
                            "payload": "USER_DEFINED_PAYLOAD"
                        }]
                    }
                    element_of_msg["title"] = recipe.name
                    element_of_msg["image_url"] = recipe.image_url
                    element_of_msg["buttons"][0]["url"] = recipe.url
                    print(element_of_msg)
                    elem_arrays.append(element_of_msg)
                    if len(elem_arrays) >= 10:
                        break
                FacebookApi.post_attachment(fbid, elem_arrays)

# Create your views here.
class Cooker(generic.View):
    def get(self, request, *args, **kwargs):
        print(self.request.GET)
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    pprint(message)
                    if not message['message'].get('is_echo'):
                        try:
                            post_facebook_message(message['sender']['id'], message['message']['text'])
                        except KeyError:
                            print("keyerror")
        return HttpResponse()