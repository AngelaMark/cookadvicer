import json , requests
VERIFY_TOKEN = "2318934571"
PAGE_ACCESS_TOKEN = "EAAD0kpLj8bEBALiqJAwI5OSn64ByZCwc44RZCjvCz76mayWM0ZCOBKjFZA1rLeZCcJ8KnnLsjomQP0VVPtg5bhToiKKx5wWmGlS3gUQxvRJ718JXURLN5OnZAbtLj1eBpYBLJCOtZCeSfWm9WJZCPV06xicwztkeCOGkZALTRHAYt1xWEfp3qafqx"

FACEBOOK_API_URL = 'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)


class FacebookApi:
    @staticmethod
    def post_attachment(fbid,elements):
        response_msg_d = \
            {
                "recipient": {
                    "id": fbid
                },
                "message": {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": elements
                        }
                    }
                }
            }

        response_msg = json.dumps(response_msg_d)
        requests.post(FACEBOOK_API_URL, headers={"Content-Type": "application/json"}, data=response_msg)

    @staticmethod
    def post_message(fbid,text):
        response_msg = json.dumps(
            {
                "recipient": {
                    "id": fbid
                },
                "message": {
                    "text": text
                }
            }
        )
        requests.post(FACEBOOK_API_URL, headers={"Content-Type": "application/json"}, data=response_msg)

