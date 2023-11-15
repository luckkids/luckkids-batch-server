import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
import os
from mysql_service import MysqlService
from slack import Slack
from time_service import Time
from dotenv import load_dotenv

# load_dotenv()   # aws lambda에선 환경변수로


def lambda_handler(event, context):
    slack = None
    try:
        slack = Slack(os.getenv("WEBHOOK_URL"))

        mysql = MysqlService(host=os.getenv("MYSQL_HOST"),
                             port=os.getenv("MYSQL_PORT"),
                             database=os.getenv("MYSQL_DATABASE"),
                             user=os.getenv("MYSQL_USER"),
                             password=os.getenv("MYSQL_PASSWORD"))

        cred = credentials.Certificate(os.getenv("FIREBASE_KEY_NAME"))
        firebase_admin.initialize_app(cred)

        result = mysql.get_mission_push(Time.get_kst_today_string(),
                                        Time.get_kst_time_string())

        for item in result:
            description = item['description']
            alert_time = item['alert_time']
            push_token = item['push_token']

            message = messaging.Message(
                notification=messaging.Notification(
                    title='LUCK-KIDS 럭키즈🍀',
                    body=f"{alert_time} '{description}'로 행운을 +1 키워보아요!"
                ),
                token=push_token,
            )
            messaging.send(message)

        return {
            'statusCode': 200,
            'body': 'Success!!',
            'endDate': str(Time.get_kst_now())
        }

    except Exception as e:
        slack.post(
            f":exclamation: *Mission_Push Batch Issue Detected!* :exclamation:\n"
            f"> *Date:* {Time.get_kst_today_string()}\n"
            f"> *EndTime:* {str(Time.get_kst_now())}\n"
            f"> *Error:* `{e}`\n"
        )

        return {
            'statusCode': 404,
            'body': e,
            'endDate': str(Time.get_kst_now())
        }
