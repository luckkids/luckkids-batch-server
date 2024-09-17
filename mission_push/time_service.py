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
        return now.strftime('%H:%M')

    @staticmethod
    def get_am_pm(time_obj):
        return "AM" if time_obj.hour < 12 else "PM"

    @staticmethod
    def format_time_with_am_pm(time):
        if isinstance(time, timedelta):
            base_time = datetime.combine(datetime.today(), datetime.min.time())
            time_obj = (base_time + time).time()
        else:
            time_obj = datetime.strptime(time, "%H:%M:%S").time()

        am_pm = Time.get_am_pm(time_obj)

        formatted_time = time_obj.strftime('%I:%M').lstrip('0')

        return f"{formatted_time}{am_pm}"
