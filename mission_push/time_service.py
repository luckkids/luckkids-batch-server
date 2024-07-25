from datetime import datetime, timedelta


class Time:
    @staticmethod
    def get_kst_now():
        return datetime.now() + timedelta(hours=9)

    @staticmethod
    def get_kst_today_string():
        today = Time.get_kst_now()
        return today.strftime('%Y-%m-%d')

    @staticmethod
    def get_kst_time_string():
        now = Time.get_kst_now()
        return now.strftime('%H:%M:%S')
