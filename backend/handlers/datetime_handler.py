from calendar import timegm
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class DatetimeHandler:
    def now(self) -> int:
        """Getting today's date as a Unix GMT timestamp

        Returns:
            int: Unix GMT timestamp
        """
        return timegm(datetime.now().timetuple()) * 1000

    def now_next_days(self, days: int) -> int:
        """Getting today's date plus a few days as a Unix GMT timestamp

        Args:
            days (int): Number of days from today's date

        Returns:
            int: Unix GMT timestamp
        """
        return timegm((datetime.now() + timedelta(days=days)).timetuple()) * 1000

    def convert_to_int(self, date: datetime) -> int:
        """Converting datetime to Unix format by GMT

        Args:
            date (datetime)

        Returns:
            int: Unix GMT timestamp
        """
        return timegm(date.timetuple()) * 1000

    def add_timedelta(self, date: int, delta: timedelta) -> datetime:
        """Adding timedelta to a date in Unix GMT format

        Args:
            date (int)
            delta (timedelta)

        Returns:
            datetime: Result
        """
        return self.convert_to_datetime(date) + delta

    def convert_to_datetime(self, date: int) -> datetime:
        """Converting Unix format by GMT to datetime

        Args:
            date (int)

        Returns:
            datetime
        """
        if date > 0:
            return datetime.fromtimestamp(date / 1000)
        else:
            return datetime(1970, 1, 1) + timedelta(seconds=date / 1000)

    def check_year_range(
        self, date_to_check: datetime, year_delta_left: int, year_delta_right: int
    ) -> bool:
        """Checks the year in the range

        Args:
            date_to_check (datetime): Date to be checked
            year_delta_left (int): Left border of the range 
            (- if earlier today and + if later today)
            year_delta_right (int): The right border of the range 
            (- if earlier today and + if later today)

        Returns:
            bool: True if the year is in the range and False otherwise
        """
        left = datetime.now() + relativedelta(years=year_delta_left)
        right = datetime.now() + relativedelta(years=year_delta_right)
        return (date_to_check >= left) and (right >= date_to_check)
