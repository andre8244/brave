import time


class TimeUtil:

    @staticmethod
    def current_time_millis():
        return int(round(time.time() * 1000))

    @staticmethod
    def format_time_seconds(seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    @staticmethod
    def format_date_time():
        return time.strftime("%Y-%m-%d_%H.%M.%S")
