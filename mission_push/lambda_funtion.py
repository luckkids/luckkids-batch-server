from mysql_service import MysqlService
from slack import Slack
from time_service import Time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
import os
import logging
# from dotenv import load_dotenv

# load_dotenv()   # aws lambda에선 환경변수로

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ID_LIST = []


def lambda_handler(event, context):
    lambda_title = "mission_push_batch"
    try:
        slack = Slack(os.getenv("WEBHOOK_URL"), main_title=lambda_title)
        mysql = MysqlService(host=os.getenv("MYSQL_HOST"),
                             port=os.getenv("MYSQL_PORT"),
                             database=os.getenv("MYSQL_DATABASE"),
                             user=os.getenv("MYSQL_USER"),
                             password=os.getenv("MYSQL_PASSWORD"))

        try:
            firebase_admin.get_app()
        except ValueError:
            cred = credentials.Certificate(cert=os.getenv("FIREBASE_KEY_NAME"))
            firebase_admin.initialize_app(credential=cred)

        result = mysql.get_mission_push(kst_time=Time.get_kst_time_string(), kst_date=Time.get_kst_today_string())

        for item in result:
            send_push(item)
            ID_LIST.append(item['id'])

        mysql.bulk_update_mission_push_date(idx_list=ID_LIST, kst_date=Time.get_kst_today_string())

        # success_message = slack.create_status_post(end_time=Time.get_kst_now())
        # slack.post(success_message)
        success_response = create_response(status_code=200,
                                           body=f"{lambda_title} success!",
                                           end_time=Time.get_kst_now())
        logger.info(success_response)

        return success_response

    except Exception as e:
        fail_message = slack.create_status_post(end_time=Time.get_kst_now(), error=e)
        slack.post(fail_message)

        fail_response = create_response(status_code=404, body=e, end_time=Time.get_kst_now())
        logger.error(fail_response)

        return fail_response


def send_push(item):
    try:
        mission_description = item['mission_description']
        mission_alert_time = item['alert_time']
        push_token = item['push_token']
        sound = item['sound']

        # iOS용 설정
        apns_config = messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    alert=messaging.ApsAlert(
                        title='LUCK-KIDS 럭키즈🍀',
                        body=f"{mission_alert_time} '{mission_description}'(으)로 행운을 +1 키워보아요!",
                    ),
                    sound=sound
                )
            )
        )

        data = {
            'screen': 'Mission'
        }

        message = messaging.Message(
            apns=apns_config,
            data=data,
            token=push_token,
        )
        messaging.send(message)

        logger.info({
            'push_token': push_token,
            'mission_description': mission_description,
            'mission_alert_time': str(mission_alert_time)
        })

    except Exception as e:
        logger.error(f"Error in send_push: {e}")


def create_response(status_code, body, end_time):
    return {
        'statusCode': status_code,
        'body': body,
        'endDate': str(end_time)
    }
