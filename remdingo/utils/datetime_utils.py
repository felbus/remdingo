import calendar
from typing import List
import datetime as dt_module
import time as time_module
from datetime import date, time, timezone
from calendar import monthrange
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd


class DatetimeUtils:
    @staticmethod
    def remove_microseconds_from_string(source: str) -> str:
        d = DatetimeUtils.convert_string_to_datetime(source)
        return DatetimeUtils.remove_microseconds_from_datetime(d)

    @staticmethod
    def remove_microseconds_from_datetime(source: datetime) -> str:
        dnm = source.replace(microsecond=0)
        return DatetimeUtils.convert_datetime_to_string(dnm).replace(".000000", "")

    @staticmethod
    def get_min_datetime_str():
        return DatetimeUtils.convert_datetime_to_string(datetime.min)

    @staticmethod
    def get_string_time_in_seconds(seconds: int) -> str:
        return f"{seconds} secs"

    @staticmethod
    def get_string_time_in_minutes(seconds: int) -> str:
        return f"{round(seconds / 60)} min {seconds  % 60} secs"

    @staticmethod
    def epoch_from_datetime(dt: datetime) -> int:
        s = DatetimeUtils.convert_datetime_to_string(dt, milliseconds=False)
        return DatetimeUtils.epoch_from_datetime_str(s)

    @staticmethod
    def epoch_from_datetime_str(dt: str) -> int:
        return int(calendar.timegm(time_module.strptime(dt, '%Y-%m-%d %H:%M:%S')))

    @staticmethod
    def epoch_from_date_str(d: str) -> int:
        return int(calendar.timegm(time_module.strptime(d, '%Y-%m-%d')))

    @staticmethod
    def datetime_from_epoch(epoch: int) -> datetime:
        return dt_module.datetime.utcfromtimestamp(epoch)

    @staticmethod
    def date_from_epoch(epoch: int) -> date:
        return dt_module.date.fromtimestamp(epoch)

    @staticmethod
    def get_current_date() -> datetime.date:
        return date.today()

    @staticmethod
    def get_local_datetime_string():
        return DatetimeUtils.convert_datetime_to_string(DatetimeUtils.get_local_datetime())

    @staticmethod
    def get_local_datetime():
        return datetime.now()

    @staticmethod
    def get_current_utc() -> datetime:
        return datetime.strptime(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def convert_datetime_to_datetime_hour(source) -> datetime:
        return source.replace(minute=0, second=0, microsecond=0)

    @staticmethod
    def get_current_utc_hour() -> datetime:
        x = DatetimeUtils.get_current_utc()
        x = x.replace(minute=0, second=0, microsecond=0)
        return x

    @staticmethod
    def get_current_utc_hour_string() -> str:
        x = DatetimeUtils.get_current_utc()
        x = x.replace(minute=0, second=0, microsecond=0)
        x = DatetimeUtils.convert_datetime_to_string(x)
        return x

    @staticmethod
    def create_date(year, month, day) -> date:
        return date(year=year, month=month, day=day)

    # @staticmethod
    #def create_datetime(year, month, day, hour, minute) -> datetime:
    #    return dt_module.datetime(year, month, day, hour, minute)

    @staticmethod
    def create_datetime(year, month, day, hour, minute) -> datetime:
        return datetime(year=year, month=month, day=day, hour=hour, minute=minute)

    @staticmethod
    def create_datetime_str(year, month, day, hour, minute) -> str:
        x = datetime(year=year, month=month, day=day, hour=hour, minute=minute)
        return DatetimeUtils.convert_datetime_to_string(x)

    @staticmethod
    def get_current_utc_string() -> str:
        return DatetimeUtils.convert_datetime_to_string(DatetimeUtils.get_current_utc())

    @staticmethod
    def get_current_time() -> datetime.time:
        return datetime.now().time()

    @staticmethod
    def create_new_time(hour: int, minute: int) -> time:
        return time(hour, minute, 0, 0)

    @staticmethod
    def get_current_date_string() -> str:
        return date.today().strftime('%Y-%m-%d')

    @staticmethod
    def get_current_datetime_string() -> str:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_backwards_datetime(days_back: int) -> datetime:
        return datetime.now() - timedelta(days=days_back)

    @staticmethod
    def get_backwards_date(days_back: int) -> datetime.date:
        x = datetime.now() - timedelta(days=days_back)
        return x.date()

    @staticmethod
    def get_backwards_datetime_string(days_back: int) -> str:
        t = datetime.now() - timedelta(days=days_back)
        return t.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def add_seconds_to_datetime(dt: datetime, seconds: int) -> datetime:
        return dt + timedelta(seconds=seconds)

    @staticmethod
    def subtract_seconds_from_datetime(dt: datetime, seconds: int) -> datetime:
        return dt - timedelta(seconds=seconds)

    @staticmethod
    def subtract_hours_from_datetime(dt: datetime, hours: int) -> datetime:
        return dt - timedelta(hours=hours)

    @staticmethod
    def subtract_minutes_from_datetime(dt: datetime, minutes: int) -> datetime:
        return dt - timedelta(minutes=minutes)

    @staticmethod
    def add_minutes_to_datetime(dt: datetime, minutes: int) -> datetime:
        return dt + timedelta(minutes=minutes)

    @staticmethod
    def add_hours_to_datetime(dt: datetime, hours: int) -> datetime:
        return dt + timedelta(hours=hours)

    @staticmethod
    def add_days_to_datetime(dt: datetime, days: int) -> datetime:
        return dt + timedelta(days=days)

    @staticmethod
    def add_weeks_to_datetime(dt: datetime, weeks: int) -> datetime:
        return dt + timedelta(weeks=weeks)

    @staticmethod
    def add_months_to_datetime(dt: datetime, months: int) -> datetime:
        return dt + relativedelta(months=months)

    @staticmethod
    def add_years_to_datetime(dt: datetime, years: int) -> datetime:
        return dt + relativedelta(years=years)

    @staticmethod
    def get_backwards_date_string(days_back: int) -> str:
        date_string = date.today() - timedelta(days=days_back)
        return date_string.strftime('%Y-%m-%d')

    @staticmethod
    def get_forward_date(days_forward: int) -> date:
        return date.today() + timedelta(days_forward)

    @staticmethod
    def get_forward_date_string(days_forward: int) -> str:
        date_string = date.today() + timedelta(days_forward)
        return date_string.strftime('%Y-%m-%d')

    @staticmethod
    def get_weekday_from_int(week_day_num: int):
        if week_day_num == 0:
            return "Sunday"
        if week_day_num == 1:
            return "Monday"
        if week_day_num == 2:
            return "Tuesday"
        if week_day_num == 3:
            return "Wednesday"
        if week_day_num == 4:
            return "Thursday"
        if week_day_num == 5:
            return "Friday"
        if week_day_num == 6:
            return "Saturday"

    @staticmethod
    def convert_np64_to_datetime(dt64: any) -> datetime:
        npts = pd.to_datetime(dt64)
        return DatetimeUtils.convert_np_timestamp_to_datetime(npts)

    @staticmethod
    def convert_np_timestamp_to_datetime(npts: any) -> datetime:
        d = npts.date()
        t = npts.time()
        return DatetimeUtils.create_datetime(d.year, d.month, d.day, t.hour, t.minute)

    @staticmethod
    def convert_timestamp_to_datetime(ts: any) -> datetime:
        return datetime.fromtimestamp(ts)

    @staticmethod
    def convert_string_to_date(date_str: str) -> date:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception as exception:
            raise exception

    @staticmethod
    def convert_string_to_datetime(datetime_str: str) -> datetime:
        try:
            if '.000000000' in datetime_str:
                datetime_str = datetime_str.replace('.000000000', '')
                datetime_str = datetime_str.replace('T', ' ')
            # JavaScript ISO format
            if "Z" in datetime_str:
                return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            elif "." in datetime_str:
                return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
            elif ":" in datetime_str:
                return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            else:
                return datetime.strptime(datetime_str, "%Y-%m-%d")
        except Exception as exception:
            raise exception

    @staticmethod
    def convert_date_to_datetime_midnight(d: date) -> datetime:
        return dt_module.datetime(d.year, d.month, d.day)

    @staticmethod
    def convert_date_to_datetime(d: date, h: int, m: int) -> datetime:
        return dt_module.datetime(d.year, d.month, d.day, h, m)

    @staticmethod
    def convert_date_str_to_datetime(d: str, h: int, m: int) -> datetime:
        return DatetimeUtils.convert_date_to_datetime(DatetimeUtils.convert_string_to_date(d), h, m)

    @staticmethod
    def convert_date_to_string(date_obj: date) -> str:
        try:
            return date_obj.strftime("%Y-%m-%d")
        except Exception as exception:
            return str(exception)

    @staticmethod
    def convert_datetime_to_string(datetime_obj: datetime, seconds: bool = True, milliseconds: bool = False) -> str:
        try:
            if milliseconds:
                return datetime_obj.strftime("%Y-%m-%d %H:%M:%S.%f")
            elif seconds:
                return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return datetime_obj.strftime("%Y-%m-%d %H:%M")
        except Exception as exception:
            return str(exception)

    @staticmethod
    def get_current_day_month_year() -> tuple:
        date_obj = date.today()
        return date_obj.day, date_obj.month, date_obj.year

    @staticmethod
    def get_day_month_year_from_date_string(date_str: str) -> tuple:
        try:
            date_obj = DatetimeUtils.convert_string_to_datetime(date_str)
            return date_obj.day, date_obj.month, date_obj.year
        except Exception as exception:
            raise exception

    @staticmethod
    def get_days_in_month_from_date_string(date_str: str) -> int:
        try:
            d = DatetimeUtils.convert_string_to_datetime(date_str)
            return DatetimeUtils.get_days_in_month_from_date(d)
        except Exception as exception:
            raise exception

    @staticmethod
    def get_days_in_month_from_date(d: date) -> int:
        try:
            return calendar.monthrange(d.year, d.month)[1]
        except Exception as exception:
            raise exception

    @staticmethod
    def get_day_month_year_string_from_date(date_obj: datetime.date) -> tuple:
        try:
            day = date_obj.day
            month = date_obj.month
            year = date_obj.year
            return str(day), str(month), str(year)
        except Exception as exception:
            raise exception

    @staticmethod
    def subtract_months_from_date(date_obj: date, months: int) -> date:
        if months > 12:
            raise Exception("Cannot subtract more than 12 months")

        # if its 4 and take 6, answer should be 10
        if date_obj.month - months < 1:
            m = 12 - (date_obj.month - months)
            y = date_obj.year - 1
        else:
            m = date_obj.month - months
            y = date_obj.year

        max_day_in_month = monthrange(y, m)[1]
        d = date_obj.day if date_obj.day < max_day_in_month else max_day_in_month
        return date_obj.replace(year=y, day=d, month=m)

    @staticmethod
    def get_date_time_from_datetime_from_date_string(date_time_str: str) -> tuple:
        try:
            date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")
            parsed_date = date_time_obj.date()
            parsed_time = date_time_obj.time()
            return parsed_date, parsed_time
        except Exception as exception:
            raise exception

    @staticmethod
    # example date_time_string = '2018-06-29 08:15:27.243860'
    def get_hour_min_from_datetime_from_date_string(date_time_str: str) -> tuple:
        try:
            date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")
            parsed_hour = date_time_obj.hour
            parsed_minute = date_time_obj.minute
            return parsed_hour, parsed_minute
        except Exception as exception:
            raise exception

    @staticmethod
    def is_date_or_datetime(d) -> bool:
        try:
            return isinstance(d, (datetime, date))
        except Exception as exception:
            raise exception

    @staticmethod
    def get_date_from_datetime(d):
        try:
            if DatetimeUtils.is_date_or_datetime(d):
                return d.date() if isinstance(d, datetime) else d
        except Exception as exception:
            raise exception

    @staticmethod
    def get_days_difference_between_dates(date1: datetime.date, date2: datetime.date, inclusive=False) -> int:
        try:
            date1 = DatetimeUtils.get_date_from_datetime(date1)
            date2 = DatetimeUtils.get_date_from_datetime(date2)
            days_difference = abs((date1 - date2).days)  # returns absolute number of days between days
            return days_difference + 1 if inclusive else days_difference
        except Exception as exception:
            raise exception

    @staticmethod
    def get_days_difference_from_current_date(from_date: datetime) -> int:
        today = date.today()
        try:
            days_difference = abs((today - from_date).days)  # returns absolute number of days from from current date
            return days_difference
        except Exception as exception:
            raise exception

    @staticmethod
    def get_seconds_difference_between_date_str(dt1: str, dt2: str) -> int:
        try:
            dt1 = DatetimeUtils.convert_string_to_datetime(dt1) if type(dt1) == str else dt1
            dt2 = DatetimeUtils.convert_string_to_datetime(dt2) if type(dt2) == str else dt2
            dt1 = pd.Timestamp(dt1)
            dt2 = pd.Timestamp(dt2)
            return int((dt2 - dt1).total_seconds())
        except Exception as exception:
            raise exception

    @staticmethod
    def get_seconds_difference_between_dates(dt1: datetime, dt2: datetime) -> int:
        try:
            return int((dt2 - dt1).total_seconds())
        except Exception as exception:
            raise exception

    @staticmethod
    def check_list_of_dates_exists(dates: List[any]) -> bool:
        return True if dates and len(dates) > 0 else False

    @staticmethod
    def is_datetime(source: any):
        return type(source) == datetime

    @staticmethod
    def check_list_of_dates_type(dates: List[datetime]) -> List[datetime]:
        if all([type(d) == datetime for d in dates]):
            return dates
        dates = [str(d) for d in dates]
        dates = DatetimeUtils.cast_dates(dates)
        return dates

    @staticmethod
    def cast_dates(dates: List[str]) -> List[datetime]:
        safe_dates = [DatetimeUtils.convert_string_to_datetime(d) for d in dates]
        return safe_dates

    @staticmethod
    def datetime_list_to_date_list(datetime_list: List[datetime]) -> List[datetime.date]:
        dates = []
        if DatetimeUtils.check_list_of_dates_exists(datetime_list):
            for item in datetime_list:
                dates.append(item.date()) if isinstance(item, datetime) else dates.append(item)
            return dates
        return []

    @staticmethod
    def datetime_list_to_str_list(datetime_list: List[datetime]) -> List[str]:
        dates = []
        if DatetimeUtils.check_list_of_dates_exists(datetime_list):
            for item in datetime_list:
                dates.append(DatetimeUtils.convert_datetime_to_string(item))
            return dates
        return []

    @staticmethod
    def datetime_list_to_date_set(datetime_list: List[datetime]) -> List[datetime.date]:
        dates = []
        if DatetimeUtils.check_list_of_dates_exists(datetime_list):
            for item in datetime_list:
                dates.append(item.date()) if isinstance(item, datetime) else dates.append(item)

        set_of_dates = set(dates)
        return list(set_of_dates)

    @staticmethod
    def build_datetime_list(dates: List[str]) -> List[datetime]:
        if DatetimeUtils.check_list_of_dates_exists(dates):
            #dts = [DatetimeUtils.convert_string_to_datetime(d) for d in dates]
            safe_dates = DatetimeUtils.check_list_of_dates_type(dates)
            safe_dates.sort()
            return safe_dates
        return []

    @staticmethod
    def get_min_max_diff(dates):
        min_date, max_date = min(dates), max(dates)
        return min_date, max_date, DatetimeUtils.get_days_difference_between_dates(min_date, max_date, True)
