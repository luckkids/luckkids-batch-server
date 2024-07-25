from datetime import datetime, timedelta


class Time:
    @staticmethod
    def get_kst_now():
        return datetime.now() + timedelta(hours=9)
