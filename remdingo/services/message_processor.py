from typing import List
import traceback
from datetime import date, time
import re
import pytz
from pytz import country_timezones

from remdingo.utils.datetime_utils import DatetimeUtils
from remdingo.storage.reminders_repo import RemindersRepo
from remdingo.services.reminder_utls import ReminderUtils

from word2number import w2n

"""
in sixty two hours get bread for someone else
in 62 hours get bread for someone else
in one hour respond to email</li>
in three days at 3pm book test</li>
in one month pay my rent</li>
at 1630 take a break</li>
tomorrow at 1630 pick up delivery</li>
next monday at 11:15am book meeting with Tom</li>
on 4th august at 2:45pm book holiday</li>
every hour do some exercises</li>
every week on tuesday at 1015 complete weekly report</li>

"""


class MessageProcessor:
    PUNCTUATION_TO_STRIP = ',.!?;:'

    @staticmethod
    def strip_punctuation(text: str) -> str:
        """Remove trailing punctuation from a string."""
        return text.rstrip(MessageProcessor.PUNCTUATION_TO_STRIP)

    @staticmethod
    def is_int(s: str):
        return s.isdigit()

    @staticmethod
    def get_country_timezones():
        timezone_country = {}

        for country_code in country_timezones:
            timezones = country_timezones[country_code]
            for timezone in timezones:
                timezone_country[timezone] = country_code

        return timezone_country

    @staticmethod
    def is_usa_timezone(s: str) -> bool:
        timezone_country = MessageProcessor.get_country_timezones()
        y = timezone_country[s]

        if y == "US":
            return True
        else:
            return False

    @staticmethod
    def regex_detect_full_d_m_y_t_with_seconds(message: str):
        dmyt = r'([0-9]{1,2})\/([0-9]{1,2})\/([0-9]{1,4})\s[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}'
        m_dmyt = re.search(dmyt, message)

        if m_dmyt:
            return True
        else:
            return False

    @staticmethod
    def check_for_dmy_date_format(message_components: List[str]):
        pattern = r'([0-9]{1,2})\/([0-9]{1,2})\/([0-9]{1,4})'
        return MessageProcessor.check_regex(message_components, pattern)

    @staticmethod
    def check_for_dm_date_format(message_components: List[str]):
        pattern = r'([0-9]{1,2})\/([0-9]{1,2})'
        return MessageProcessor.check_regex(message_components, pattern)

    @staticmethod
    def check_for_time_format(message_components: List[str]):
        # 24hour
        pattern = r'^([0-1]?[0-9]|2[0-3])(:)?[0-5][0-9](\s*[aApP]mM)?$'
        found, position, prefix = MessageProcessor.check_regex(message_components, pattern)

        if not found:
            # 12 hr
            # pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]\s?((?:[Aa]|[Pp])\.?[Mm]\.?)$'
            pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]\s?((?:[Aa]|[Pp])\.?[Mm]\.?)$'
            found, position, prefix = MessageProcessor.check_regex(message_components, pattern)

        if not found:
            # only hour up to 12 with AM|PM
            pattern = r'^(0?[1-9]|1[0-2])([Aa|Pp][Mm])$'
            found, position, prefix = MessageProcessor.check_regex(message_components, pattern)

        return found, position, prefix

    @staticmethod
    def check_regex(message_components: List[str], pattern):
        found_position = 0
        for x in message_components:
            found_pattern = re.search(pattern, x)
            if found_pattern:
                return True, found_position, "/"
            found_position = found_position + 1
        return False, 0, ""

    @staticmethod
    def get_time_periods():
        return ['m', 'min', 'mins', 'minute', 'minutes', 'hr', 'hrs', 'hour', 'hours', 'd', 'day', 'days', 'w', 'wk', 'wks', 'week', 'weeks', 'month', 'month', 'y', 'year', 'years']

    @staticmethod
    def get_months():
        return ['jan', 'january', 'feb', 'february', 'mar', 'march', 'apr', 'april', 'may', 'jun', 'june', 'jul', 'july', 'aug', 'august', 'sep', 'september', 'oct', 'october', 'nov', 'november', 'dec', 'december']

    @staticmethod
    def get_days_of_week():
        return ['mon', 'monday', 'tues', 'tuesday', 'weds', 'wednesday', 'thurs', 'thursday', 'fri', 'friday', 'sat', 'saturday', 'sun', 'sunday']

    @staticmethod
    def get_days_of_week_index(day: str) -> int:
        day_dict = {
            'mon': 0, 'monday': 0,
            'tue': 1, 'tues': 1, 'tuesday': 1,
            'wed': 2, 'weds': 2, 'wednesday': 2,
            'thur': 3, 'thurs': 3, 'thursday': 3,
            'fri': 4, 'friday': 4,
            'sat': 5, 'saturday': 5,
            'sun': 6, 'sunday': 6,
        }

        return day_dict[day.lower()]

    @staticmethod
    def get_month_index(month: str) -> int:
        months_dict = {
                'jan': 1, 'january': 1,
                'feb': 2, 'february': 2,
                'mar': 3, 'march': 3,
                'apr': 4, 'april': 4,
                'may': 5,
                'jun': 6, 'june': 6,
                'jul': 7, 'july': 7,
                'aug': 8, 'august': 8,
                'sep': 9, 'september': 9,
                'oct': 10, 'october': 10,
                'nov': 11, 'november': 11,
                'dec': 12, 'december': 12
            }

        return months_dict[month.lower()]

    @staticmethod
    def get_month_day_suffixes():
        return ['st', 'nd', 'th', 'rd', 'nd']

    @staticmethod
    def count_number_of_time_periods(message_components: List[str]) -> int:
        count = 0
        for x in message_components:
            if x in MessageProcessor.get_time_periods():
                count = count + 1
        return count

    @staticmethod
    def get_month_location(message_components: List[str]) -> int:
        months = MessageProcessor.get_months()
        loop_count = 0
        month_location = 0
        for element in message_components:
            if element in months:
                month_location = loop_count
                break
            loop_count = loop_count + 1
        return month_location

    @staticmethod
    def get_time_period_location(message_components: List[str], occurrence: int) -> int:
        # find minute(s) | hour(s) | day(s) | week(s) | month(s) | year(s)
        time_periods = MessageProcessor.get_time_periods()
        loop_count = 0
        time_period_location = 0
        found = 0
        for element in message_components:
            # print(f"looking: {loop_count}")
            if element in time_periods:
                time_period_location = loop_count
                found = found + 1
            if found == occurrence:
                break
            loop_count = loop_count + 1
        return time_period_location

    @staticmethod
    def add_time_to_datetime(source_datetime, time_period: str, number: int) -> any:
        reminder_datetime = source_datetime

        if time_period in ['min', 'mins', 'minute', 'minutes']:
            reminder_datetime = DatetimeUtils.add_minutes_to_datetime(source_datetime, number)
        if time_period in ['hr', 'hrs', 'hour', 'hours']:
            reminder_datetime = DatetimeUtils.add_hours_to_datetime(source_datetime, number)
        if time_period in ['day', 'days']:
            reminder_datetime = DatetimeUtils.add_days_to_datetime(source_datetime, number)
        if time_period in ['wk', 'wks', 'week', 'weeks']:
            reminder_datetime = DatetimeUtils.add_weeks_to_datetime(source_datetime, number)
        if time_period in ['month', 'months']:
            reminder_datetime = DatetimeUtils.add_months_to_datetime(source_datetime, number)
        if time_period in ['year', 'years']:
            reminder_datetime = DatetimeUtils.add_years_to_datetime(source_datetime, number)
        return reminder_datetime

    @staticmethod
    def get_time_element(message_components: List[str], time_element_occurrence: int, start_position: int):
        # time element is "one hour" "two days" "30 minutes" - a combinations of a number and a time period

        if message_components[start_position].lower() == "and":
            start_position = start_position + 1

        time_period_location = MessageProcessor.get_time_period_location(message_components, time_element_occurrence)

        # if format is "in X (hours|minutes|..)" - is X a string or an int?
        if MessageProcessor.is_int(message_components[time_period_location - 1]):
            # if int and it only occupies one element, get the number
            number = int(message_components[time_period_location - 1])
        else:
            # otherwise its a string, get all elements and convert to number
            number_str = " ".join(message_components[start_position:time_period_location])
            number = w2n.word_to_num(number_str)

        print(f"time element {number} {MessageProcessor.get_time_periods()[time_period_location]} ")
        time_period = message_components[time_period_location]

        return time_period_location, time_period, number

    @staticmethod
    def get_time_from_string(time_str: str) -> any:
        hr = 100000
        m = 100000

        time_str = time_str.lower()

        found_valid_time = MessageProcessor.check_for_time_format([time_str])

        if not found_valid_time:
            return 0

        time_str_no_am_pm = time_str.replace("am", "")
        time_str_no_am_pm = time_str_no_am_pm.replace("pm", "")

        if ("am" in time_str or "pm" in time_str) and ":" not in time_str and len(time_str_no_am_pm) < 3:
            hr = int(time_str_no_am_pm)
            m = 0
        else:
            if len(time_str_no_am_pm) == 4 and ":" not in time_str_no_am_pm:
                hr = int(time_str_no_am_pm[0:2])
                m = int(time_str_no_am_pm[2:4])
            elif len(time_str_no_am_pm) == 2 and ":" not in time_str_no_am_pm:
                hr = int(time_str_no_am_pm[0:2])
                m = 0
            elif len(time_str_no_am_pm) == 1 and ":" not in time_str_no_am_pm:
                hr = int(time_str_no_am_pm[0:1])
                m = 0
            elif ":" in time_str_no_am_pm:
                hr = int(time_str_no_am_pm[0:time_str_no_am_pm.index(":")])
                m = int(time_str_no_am_pm[time_str_no_am_pm.index(":")+1:len(time_str_no_am_pm)])

        if "pm" in time_str.lower() and hr < 12:
            hr = hr + 12

        t = time(hr, m)

        return t

    @staticmethod
    def check_str_contains_month_day_suffix(s: str):
        for x in MessageProcessor.get_month_day_suffixes():
            if x in s:
                return True

    @staticmethod
    def remove_month_day_suffix(s: str):
        for x in MessageProcessor.get_month_day_suffixes():
            if x in s:
                s = s.replace(x, "")
                return s

    @staticmethod
    def extract_month_day_year(message_components: List[str], month_location: int, base_dt=DatetimeUtils.get_current_utc()):
        month = message_components[month_location]
        month_index = MessageProcessor.get_month_index(month)

        if month_location > 0:
            # does component before or after month contain th st rd nd
            day_str = "0"
            day_location = 0

            if MessageProcessor.check_str_contains_month_day_suffix(message_components[month_location + 1]):
                day_location = month_location + 1
                day_str = MessageProcessor.remove_month_day_suffix(message_components[month_location + 1])
            elif MessageProcessor.check_str_contains_month_day_suffix(message_components[month_location - 1]):
                day_location = month_location - 1
                day_str = MessageProcessor.remove_month_day_suffix(message_components[month_location - 1])
            elif MessageProcessor.is_int(message_components[month_location + 1]):
                day_location = month_location + 1
                day_str = message_components[month_location + 1]
            elif MessageProcessor.is_int(message_components[month_location - 1]):
                day_location = month_location - 1
                day_str = message_components[month_location - 1]

            day = int(day_str)

            if month_location > day_location:
                year_location = month_location + 1
            else:
                year_location = day_location + 1

            if MessageProcessor.is_int(message_components[year_location]):
                y = int(message_components[year_location])
                if 2000 < y < 3000:
                    return DatetimeUtils.create_date(y, month_index, day), year_location + 1

            # if there is no year, and the month in the message is greater than current month
            # then year should be next year. ie it might be december, and someone writes jan 5th
            y = base_dt.year
            if month_index < base_dt.month:
                y = base_dt.year + 1

            if day_location > month_location:
                return DatetimeUtils.create_date(y, month_index, day), day_location + 1
            else:
                return DatetimeUtils.create_date(y, month_index, day), month_location + 1

    @staticmethod
    def process_message(message: str, offset: int, tz="", base_dt=None):
        message = message.lower()
        message_components = [MessageProcessor.strip_punctuation(word) for word in message.split(' ')]

        # time periods are if someone said hours, hrs, mins, weeks, etc.. not actual times like 09:15
        number_of_time_periods = MessageProcessor.count_number_of_time_periods(message_components)

        print(message_components)

        # base_dt used for testing purposes
        if base_dt is None:
            base_dt = DatetimeUtils.get_current_utc()

        reminder_date_utc = base_dt
        reminder_date_user = DatetimeUtils.add_minutes_to_datetime(base_dt, offset)
        time_period_location = 0
        message_str = ""
        success = True

        if message_components[0] == "yesterday":
            return reminder_date_utc, reminder_date_user, "cannot set reminders in the past", False

        # uses time periods, in one hour, etc..
        if message_components[0] == "in":
            start_position = 1
            for time_element_occurrence in range(1, number_of_time_periods + 1):
                time_period_location, time_period, number = MessageProcessor.get_time_element(message_components, time_element_occurrence, start_position)
                start_position = time_period_location + 1
                reminder_date_utc = MessageProcessor.add_time_to_datetime(reminder_date_utc, time_period, number)

            reminder_date_user = DatetimeUtils.add_minutes_to_datetime(reminder_date_utc, offset)
            message_str = " ".join(message_components[time_period_location + 1:len(message_components)])

        if MessageProcessor.check_for_time_format([message_components[0]])[0]:
            reminder_date_utc, reminder_date_user, message_str = MessageProcessor.get_reminder_for_date_time(message_components, offset, reminder_date_user, tz, starts_with_time=True)

        # uses real times ie; 09:15
        if message_components[0] == "at":
            reminder_date_utc, reminder_date_user, message_str = MessageProcessor.get_reminder_for_date_time(message_components, offset, reminder_date_user, tz)

        if message_components[0] == "on":
            # check is month day year is words or dd/mm/yyyy type format
            month_location = MessageProcessor.get_month_location(message_components)
            dmy = MessageProcessor.check_for_dmy_date_format(message_components)
            dm = MessageProcessor.check_for_dm_date_format(message_components)

            # using words
            if month_location > 0:
                d, time_start = MessageProcessor.extract_month_day_year(message_components, month_location, base_dt)

                if message_components[time_start].lower() != "at":
                    time_start = time_start - 1

                t = MessageProcessor.get_time_from_string(message_components[time_start+1])
                reminder_date_user = DatetimeUtils.create_datetime(d.year, d.month, d.day, t.hour, t.minute)
                message_str = " ".join(message_components[time_start+2:len(message_components)])
            # using dd/mm/yyyy
            elif dmy[0]:
                time_start = dmy[1]+2

                if message_components[time_start].lower() != "at":
                    time_start = time_start - 1

                t = MessageProcessor.get_time_from_string(message_components[time_start])

                if MessageProcessor.is_usa_timezone(tz):
                    mdy_dt = message_components[dmy[1]].split(dmy[2])
                    reminder_date_user = DatetimeUtils.create_datetime(int(mdy_dt[2]), int(mdy_dt[0]), int(mdy_dt[1]), t.hour, t.minute)
                    message_str = " ".join(message_components[time_start+1:len(message_components)])
                else:
                    dmy_dt = message_components[dmy[1]].split(dmy[2])
                    reminder_date_user = DatetimeUtils.create_datetime(int(dmy_dt[2]), int(dmy_dt[1]), int(dmy_dt[0]), t.hour, t.minute)
                    message_str = " ".join(message_components[time_start+1:len(message_components)])
            # using dd/mm
            elif dm[0]:
                time_start = dm[1]+2

                if message_components[time_start].lower() != "at":
                    time_start = time_start - 1

                t = MessageProcessor.get_time_from_string(message_components[time_start])

                if MessageProcessor.is_usa_timezone(tz):
                    md_dt = message_components[dm[1]].split(dm[2])
                    reminder_date_user = DatetimeUtils.create_datetime(base_dt.year, int(md_dt[0]), int(md_dt[1]), t.hour, t.minute)
                    message_str = " ".join(message_components[time_start+1:len(message_components)])
                else:
                    dm_dt = message_components[dm[1]].split(dm[2])
                    reminder_date_user = DatetimeUtils.create_datetime(base_dt.year, int(dm_dt[1]), int(dm_dt[0]), t.hour, t.minute)
                    message_str = " ".join(message_components[time_start+1:len(message_components)])
            else:
                message_str = "No month and day found"
                success = False

            reminder_date_utc = DatetimeUtils.subtract_minutes_from_datetime(reminder_date_user, offset)

        if message_components[0] == "tomorrow":
            reminder_date_user, reminder_date_utc, message_str = MessageProcessor.reminder_for_tomorrow(message_components, reminder_date_utc, offset)

        if message_components[0] in MessageProcessor.get_days_of_week():
            reminder_date_user, reminder_date_utc, message_str = MessageProcessor.reminder_for_day_in_week(message_components, reminder_date_utc, offset)

        if message_components[0] == "next" and message_components[1] in MessageProcessor.get_days_of_week():
            reminder_date_user, reminder_date_utc, message_str = MessageProcessor.reminder_for_day_in_week(message_components, reminder_date_utc, offset, 1)
            reminder_date_user = DatetimeUtils.add_days_to_datetime(reminder_date_user, 7)
            reminder_date_utc = DatetimeUtils.add_days_to_datetime(reminder_date_utc, 7)

        if message_components[0] == "every":
            number = message_components[1]

        if reminder_date_utc < base_dt:
            message_str = "reminder is in the past"
            success = False

        if message_str == "":
            success = False

        return reminder_date_utc, reminder_date_user, message_str, success

    @staticmethod
    def get_reminder_for_date_time(message_components, offset, base_dt, tz, starts_with_time=False):
        # check is month day year is words or dd/mm/yyyy type format
        month_location = MessageProcessor.get_month_location(message_components)
        dmy = MessageProcessor.check_for_dmy_date_format(message_components)
        dm = MessageProcessor.check_for_dm_date_format(message_components)

        # if this statement is true then it is something like
        # 9am do some errand
        if starts_with_time and not dmy[0] and not dm[0] and month_location == 0:
            t = MessageProcessor.get_time_from_string(message_components[0])

            # if hour is > than now, then reminder is for today, otherwise its for tomorrow
            # eg its 6pm now and reminder is for 9am, then its 9am tomorrow
            if base_dt.hour > t.hour or base_dt.hour == t.hour and base_dt.minute > t.minute:
                reminder_date_user_tomorrow = DatetimeUtils.add_days_to_datetime(base_dt, 1)
                reminder_date_user = DatetimeUtils.create_datetime(
                    reminder_date_user_tomorrow.year, reminder_date_user_tomorrow.month, reminder_date_user_tomorrow.day, t.hour, t.minute
                )
            else:
                reminder_date_user = DatetimeUtils.create_datetime(
                    base_dt.year, base_dt.month, base_dt.day, t.hour, t.minute
                )

            reminder_date_utc = DatetimeUtils.subtract_minutes_from_datetime(reminder_date_user, offset)
            message_str = " ".join(message_components[1:len(message_components)])
            return reminder_date_utc, reminder_date_user, message_str

        # if at is first word then the next things should be a time (could be followed by on a date)
        t = MessageProcessor.get_time_from_string(message_components[1])

        # using words
        if month_location > 0:
            d, message_start = MessageProcessor.extract_month_day_year(message_components, month_location, base_dt)
            reminder_date_user = DatetimeUtils.create_datetime(d.year, d.month, d.day, t.hour, t.minute)
            message_str = " ".join(message_components[message_start:len(message_components)])
        # using dd/mm/yyyy
        elif dmy[0]:
            if MessageProcessor.is_usa_timezone(tz):
                mdy_dt = message_components[dmy[1]].split(dmy[2])
                reminder_date_user = DatetimeUtils.create_datetime(int(mdy_dt[2]), int(mdy_dt[0]), int(mdy_dt[1]), t.hour, t.minute)
                message_str = " ".join(message_components[dmy[1]+1:len(message_components)])
            else:
                dmy_dt = message_components[dmy[1]].split(dmy[2])
                reminder_date_user = DatetimeUtils.create_datetime(int(dmy_dt[2]), int(dmy_dt[1]), int(dmy_dt[0]), t.hour, t.minute)
                message_str = " ".join(message_components[dm[1]+1:len(message_components)])
        # using dd/mm
        elif dm[0]:
            if MessageProcessor.is_usa_timezone(tz):
                md_dt = message_components[dm[1]].split(dm[2])
                reminder_date_user = DatetimeUtils.create_datetime(base_dt.year, int(md_dt[0]), int(md_dt[1]), t.hour, t.minute)
                message_str = " ".join(message_components[dm[1]+1:len(message_components)])
            else:
                dm_dt = message_components[dm[1]].split(dm[2])
                reminder_date_user = DatetimeUtils.create_datetime(base_dt.year, int(dm_dt[1]), int(dm_dt[0]), t.hour, t.minute)
                message_str = " ".join(message_components[dm[1]+1:len(message_components)])
        else:
            reminder_date_user = DatetimeUtils.create_datetime(base_dt.year, base_dt.month, base_dt.day, t.hour, t.minute)
            message_start = 2
            message_str = " ".join(message_components[message_start:len(message_components)])

        reminder_date_utc = DatetimeUtils.subtract_minutes_from_datetime(reminder_date_user, offset)
        return reminder_date_utc, reminder_date_user, message_str

    @staticmethod
    def reminder_for_tomorrow(message_components, reminder_date_utc, offset):
        reminder_date_user = DatetimeUtils.add_minutes_to_datetime(reminder_date_utc, offset)
        reminder_date_user = DatetimeUtils.add_days_to_datetime(reminder_date_user, 1)

        if message_components[1].lower() == "at":
            t = MessageProcessor.get_time_from_string(message_components[2])
            time_location = 2
        else:
            try:
                t = MessageProcessor.get_time_from_string(message_components[1])
                time_location = 1
            except Exception as e:
                time_location = 0
                t = time(9, 0)

        reminder_date_user = DatetimeUtils.create_datetime(reminder_date_user.year, reminder_date_user.month, reminder_date_user.day, t.hour, t.minute)
        reminder_date_utc = DatetimeUtils.subtract_minutes_from_datetime(reminder_date_user, offset)
        message_str = " ".join(message_components[time_location+1:len(message_components)])
        return reminder_date_user, reminder_date_utc, message_str

    @staticmethod
    def reminder_for_day_in_week(message_components, reminder_date_utc, offset, dow_index=0):
        reminder_date_user = DatetimeUtils.add_minutes_to_datetime(reminder_date_utc, offset)
        current_day_index = reminder_date_user.weekday()
        reminder_day_index = MessageProcessor.get_days_of_week_index(message_components[dow_index])

        days_to_add = ReminderUtils.get_days_to_add(current_day_index, reminder_day_index)

        reminder_date_user = DatetimeUtils.add_minutes_to_datetime(reminder_date_utc, offset)
        reminder_date_user = DatetimeUtils.add_days_to_datetime(reminder_date_user, days_to_add)

        time_location = dow_index

        if message_components[dow_index+1].lower() == "at":
            time_location = dow_index+2
            t = MessageProcessor.get_time_from_string(message_components[time_location])
        else:
            time_location = dow_index+1

            if MessageProcessor.check_for_time_format(message_components[time_location])[0]:
                t = MessageProcessor.get_time_from_string(message_components[time_location])
            else:
                t = time(9, 0)

        reminder_date_user = DatetimeUtils.create_datetime(reminder_date_user.year, reminder_date_user.month, reminder_date_user.day, t.hour, t.minute)
        reminder_date_utc = DatetimeUtils.subtract_minutes_from_datetime(reminder_date_user, offset)
        message_str = " ".join(message_components[time_location:len(message_components)])
        return reminder_date_user, reminder_date_utc, message_str

    @staticmethod
    def store(customer_id, reminder_date_utc, reminder_date_user, message_str, offset: int, tz: str):
        created = DatetimeUtils.get_local_datetime_string()
        reminder_date_utc = DatetimeUtils.convert_datetime_to_string(reminder_date_utc)
        reminder_date_user = DatetimeUtils.convert_datetime_to_string(reminder_date_user)
        RemindersRepo.save_reminder(customer_id, reminder_date_utc, reminder_date_user, message_str, created, offset, tz)

    @staticmethod
    def process_and_store_message(customer_id: str, message: str, offset: int, tz: str):
        try:
            reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, tz=tz)

            if success:
                MessageProcessor.store(customer_id, reminder_date_utc, reminder_date_user, message_str, offset, tz=tz)
                return f"reminder set for {reminder_date_user}, {message_str}"
            else:
                if message_str:
                    return message_str
                else:
                    return f'woops could not save the reminder: "{message}"'
        except Exception as e:
            print(traceback.format_exc())
            return traceback.format_exc()

