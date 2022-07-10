from calendar import timegm
from datetime import datetime, timedelta


class DatetimeHandler:
    def now(self) -> int:
        return timegm(datetime.now().timetuple())

    def now_next_days(self, days) -> int:
        return timegm((datetime.now() + timedelta(days=days)).timetuple())

    def convert_to_int(self, date: datetime) -> int:
        return timegm(date.timetuple())

    def add_timedelta(self, date: int, delta: timedelta) -> datetime:
        return datetime.utcfromtimestamp(date) + delta
