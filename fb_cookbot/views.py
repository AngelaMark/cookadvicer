from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.http.response import HttpResponse


import json, random, requests, re
from pprint import pprint

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

VERIFY_TOKEN = "2318934571"
PAGE_ACCESS_TOKEN = "EAAD0kpLj8bEBAHU2JvK0xtzcqAyJoU0dTTlFuPH8KQBprpWVSBwM4frgi1ZC4Ra0QFDrqgmiMzzezORYVU9L627oKJ8rvS88rpDFrGrdQanBrRMjJKk6qankZCOdJzYsJjhsHuuRw3NcnP3dTPOYxgkaJjFyZBPt2quA2qDOSXajSYQdWKw"
def post_facebook_message(fbid):

    recevied_message = "Hello"
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())


class Cooker(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '2318934571':
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
                    post_facebook_message(message['sender']['id'])
        return HttpResponse()