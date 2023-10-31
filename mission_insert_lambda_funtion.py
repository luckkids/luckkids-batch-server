from mysql_service import MysqlService
from slack import Slack
from time_service import Time
import os
# from dotenv import load_dotenv

# load_dotenv()   # aws lambda에선 환경변수로


def lambda_handler(event, context):
    slack = None
    try:
        mysql = MysqlService(host=os.getenv("MYSQL_HOST"),
                             port=os.getenv("MYSQL_PORT"),
                             database=os.getenv("MYSQL_DATABASE"),
                             user=os.getenv("MYSQL_USER"),
                             password=os.getenv("MYSQL_PASSWORD"))
        slack = Slack(os.getenv("WEBHOOK_URL"))

        result = init_default(mysql.get_mission())
        mysql.bulk_insert(result)

        slack.post(
            f":tada: *Mission Batch Success!* :tada:\n"
            f"> *Date:* {Time.get_kst_today_string()}\n"
            f"> *EndTime:* {str(Time.get_kst_now())}\n"
        )

        return {
            'statusCode': 200,
            'body': 'Success!!',
            'endDate': str(Time.get_kst_now())
        }

    except Exception as e:
        slack.post(
            f":exclamation: *Mission Batch Issue Detected!* :exclamation:\n"
            f"> *Date:* {Time.get_kst_today_string()}\n"
            f"> *EndTime:* {str(Time.get_kst_now())}\n"
            f"> *Error:* `{e}`\n"
        )

        return {
            'statusCode': 404,
            'body': e,
            'endDate': Time.get_kst_now()
        }


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
