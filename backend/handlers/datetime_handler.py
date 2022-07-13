from calendar import timegm
from datetime import datetime, timedelta


class DatetimeHandler:
    def now(self) -> int:
        """Getting today's date as a Unix GMT timestamp

        Returns:
            int: Unix GMT timestamp
        """
        return timegm(datetime.now().timetuple())

    def now_next_days(self, days: int) -> int:
        """Getting today's date plus a few days as a Unix GMT timestamp

        Args:
            days (int): Number of days from today's date

        Returns:
            int: Unix GMT timestamp
        """        
        return timegm((datetime.now() + timedelta(days=days)).timetuple())

    def convert_to_int(self, date: datetime) -> int:
        """Converting datetime to Unix format by GMT

        Args:
            date (datetime)

        Returns:
            int: Unix GMT timestamp
        """        
        return timegm(date.timetuple())

    def add_timedelta(self, date: int, delta: timedelta) -> datetime:
        """Adding timedelta to a date in Unix GMT format

        Args:
            date (int)
            delta (timedelta)

        Returns:
            datetime: Result
        """        
        return datetime.utcfromtimestamp(date) + delta
