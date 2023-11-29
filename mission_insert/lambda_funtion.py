from mysql_service import MysqlService
from slack import Slack
from time_service import Time
import os
import logging
# from dotenv import load_dotenv

# load_dotenv()   # aws lambda에선 환경변수로

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    lambda_title = "mission_insert_batch"
    try:
        slack = Slack(webhook_url=os.getenv("WEBHOOK_URL"), main_title=lambda_title)

        mysql = MysqlService(host=os.getenv("MYSQL_HOST"),
                             port=os.getenv("MYSQL_PORT"),
                             database=os.getenv("MYSQL_DATABASE"),
                             user=os.getenv("MYSQL_USER"),
                             password=os.getenv("MYSQL_PASSWORD"))

        result = init_default(mysql.get_mission())
        mysql.bulk_insert(result)

        success_message = slack.create_status_post(end_time=Time.get_kst_now())
        slack.post(success_message)

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


def init_default(missions):
    records = []

    kst_now = Time.get_kst_now()
    today_string = Time.get_kst_today_string()

    for record in missions:
        new_record = {
            'created_date': kst_now,
            'updated_date': kst_now,
            'mission_date': today_string,
            'mission_status': "FAILED",
            'mission_id': record['id']
        }
        records.append(new_record)

    return records


def create_response(status_code, body, end_time):
    return {
        'statusCode': status_code,
        'body': body,
        'endDate': str(end_time)
    }
