import json, requests, random, re
from pprint import pprint

from django.db.models import Q, Count
from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from fb_cookbot.models import Recipe, Ingredient

VERIFY_TOKEN = "2318934571"
PAGE_ACCESS_TOKEN = "EAAD0kpLj8bEBALiqJAwI5OSn64ByZCwc44RZCjvCz76mayWM0ZCOBKjFZA1rLeZCcJ8KnnLsjomQP0VVPtg5bhToiKKx5wWmGlS3gUQxvRJ718JXURLN5OnZAbtLj1eBpYBLJCOtZCeSfWm9WJZCPV06xicwztkeCOGkZALTRHAYt1xWEfp3qafqx"

# Helper function
def post_facebook_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
    # tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()

    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()

    ingredients_list = recevied_message.split(',')
    print(ingredients_list)
    excluded_ingredients = Ingredient.objects.exclude(name__in=ingredients_list)
    print(excluded_ingredients)
    recipes = Recipe.objects.filter(ingredients__name__in=ingredients_list).exclude(ingredients=excluded_ingredients).distinct()
    print(recipes)
    '''answer = ''

    for recipe in recipes:
        answer = 'Dear ' + str(user_details['first_name']) + ' you can cook:\n' + answer + recipe.name + '\n' + recipe.url + '\n'

    answer = 'Dear ' + str(user_details['first_name']) + ' you can cook:\n' '''

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % PAGE_ACCESS_TOKEN
    msg = {
        "recipient":{
                   "id":fbid
            },
        "message":{
           "attachment":{
                    "type":"template",
                    "payload":{
                        "template_type":"generic",
                        "elements":[]
                        }
                    }
                }
    }
    elem_arrays = msg['message']["attachment"]["payload"]["elements"]
    for recipe in recipes:
        element_of_msg = {
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
    response_msg = json.dumps(msg)
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

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
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly.
                    try:
                        post_facebook_message(message['sender']['id'], message['message']['text'])
                    except KeyError:
                        print("keyerror")
        return HttpResponse()
