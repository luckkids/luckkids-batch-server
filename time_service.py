from datetime import datetime, timedelta


class Time:
    @staticmethod
    def get_kst_now():
        return datetime.now() + timedelta(hours=9)

    @staticmethod
    def get_kst_today_string():
        today = Time.get_kst_now()
        today_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
        return today_date.strftime('%Y-%m-%d')
