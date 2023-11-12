from urllib.request import Request, urlopen
from json import dumps


class Slack:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def post(self, message):
        try:
            send_data = {
                "text": message,
            }
            send_text = dumps(send_data)
            request = Request(
                self.webhook_url,
                data=send_text.encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )

            with urlopen(request) as response:
                return response.read()
        except Exception as e:
            raise Exception(f"slack post Exception : {e}")
