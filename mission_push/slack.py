from urllib.request import Request, urlopen
from json import dumps


class Slack:
    def __init__(self, webhook_url, main_title):
        self.webhook_url = webhook_url
        self.main_title = main_title

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

    def create_status_post(self, end_time, error=None):
        if not error:
            message = (
                f":tada: *{self.main_title} success!* :tada:\n"
                f"> *EndTime:* {str(end_time)}\n"
            )
        else:
            message = (
                f":exclamation: *{self.main_title} Issue Detected!* :exclamation:\n"
                f"> *EndTime:* {str(end_time)}\n"
                f"> *Error:* `{error}`\n"
            )
        return message
