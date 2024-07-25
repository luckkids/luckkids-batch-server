from datetime import datetime, timedelta


class Time:
    @staticmethod
    def get_kst_now():
        return datetime.now() + timedelta(hours=9)

    @staticmethod
    def get_kst_hour_string():
        now = Time.get_kst_now()
        hour = now.replace(minute=0, second=0, microsecond=0)
        return hour.strftime('%H:%M:%S')
