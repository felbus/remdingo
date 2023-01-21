from remdingo.storage.reminders_repo import RemindersRepo
from remdingo.utils.datetime_utils import DatetimeUtils
from remdingo.services.reminder_utls import ReminderUtils

import pandas as pd

"""
in sixty two hours get bread for someone else
in 62 hours get bread for someone else
"""


class RemindersCheck:
    @staticmethod
    def get_reminder_id_from_ack(ack: str) -> int:
        x = ack.split("_", 1)[1]
        return int(x)

    @staticmethod
    def check_reminders(customer_id: str):
        reminders_df = RemindersRepo.check_reminders(customer_id)

        reminders = []
        if len(reminders_df) > 0:
            for idx, row in reminders_df.iterrows():
                reminders.append({
                    'reminder': row['reminder_text'],
                    'dt': row['reminder_date_user'],
                    'reminder_id': row['id'],
                })

        return reminders

    @staticmethod
    def process_reminder_ack(customer_id: str, ack: str, offset: int):
        id = RemindersCheck.get_reminder_id_from_ack(ack)

        if "done_" in ack:
            RemindersRepo.ack_reminder(customer_id, id)
            return "set reminder to done"
        else:
            # r = RemindersRepo.get_reminder(customer_id, id)
            reminder_date_utc_snoozed, reminder_date_user_snoozed = RemindersCheck.process_reminder_snooze(ack, offset)
            RemindersCheck.snooze_reminder(customer_id, id, reminder_date_utc_snoozed, reminder_date_user_snoozed)
            return f"snoozed reminder until {reminder_date_user_snoozed}"

    @staticmethod
    def process_reminder_snooze(ack: str, offset: int, base_dt=None):
        if base_dt:
            utc_reminder = base_dt
            user_reminder = DatetimeUtils.add_minutes_to_datetime(utc_reminder, offset)
        else:
            utc_reminder = DatetimeUtils.get_current_utc()
            user_reminder = DatetimeUtils.add_minutes_to_datetime(utc_reminder, offset)

        if "fivemins_" in ack:
            reminder_date_utc_snoozed = DatetimeUtils.add_minutes_to_datetime(utc_reminder, 5)
            reminder_date_user_snoozed = DatetimeUtils.add_minutes_to_datetime(user_reminder, 5)
            return reminder_date_utc_snoozed, reminder_date_user_snoozed
        if "15mins_" in ack:
            reminder_date_utc_snoozed = DatetimeUtils.add_minutes_to_datetime(utc_reminder, 15)
            reminder_date_user_snoozed = DatetimeUtils.add_minutes_to_datetime(user_reminder, 15)
            return reminder_date_utc_snoozed, reminder_date_user_snoozed
        if "30mins_" in ack:
            reminder_date_utc_snoozed = DatetimeUtils.add_minutes_to_datetime(utc_reminder, 30)
            reminder_date_user_snoozed = DatetimeUtils.add_minutes_to_datetime(user_reminder, 30)
            return reminder_date_utc_snoozed, reminder_date_user_snoozed
        if "1hr_" in ack:
            reminder_date_utc_snoozed = DatetimeUtils.add_minutes_to_datetime(utc_reminder, 60)
            reminder_date_user_snoozed = DatetimeUtils.add_minutes_to_datetime(user_reminder, 60)
            return reminder_date_utc_snoozed, reminder_date_user_snoozed
        if "3hrs_" in ack:
            reminder_date_utc_snoozed = DatetimeUtils.add_minutes_to_datetime(utc_reminder, 180)
            reminder_date_user_snoozed = DatetimeUtils.add_minutes_to_datetime(user_reminder, 180)
            return reminder_date_utc_snoozed, reminder_date_user_snoozed
        if "tomorrow_" in ack:
            reminder_date_user_snoozed = DatetimeUtils.add_days_to_datetime(user_reminder, 1)

            reminder_date_user_snoozed = DatetimeUtils.create_datetime(
                reminder_date_user_snoozed.year, reminder_date_user_snoozed.month, reminder_date_user_snoozed.day, 9, 0
            )

            reminder_date_utc_snoozed = DatetimeUtils.subtract_minutes_from_datetime(reminder_date_user_snoozed, offset)
            return reminder_date_utc_snoozed, reminder_date_user_snoozed
        if "monday_" in ack:
            current_day_index = user_reminder.weekday()
            reminder_day_index = 0

            days_to_add = ReminderUtils.get_days_to_add(current_day_index, reminder_day_index)
            reminder_date_user_snoozed = DatetimeUtils.add_days_to_datetime(user_reminder, days_to_add)

            reminder_date_user_snoozed = DatetimeUtils.create_datetime(
                reminder_date_user_snoozed.year, reminder_date_user_snoozed.month, reminder_date_user_snoozed.day, 9, 0
            )

            reminder_date_utc_snoozed = DatetimeUtils.subtract_minutes_from_datetime(reminder_date_user_snoozed, offset)
            return reminder_date_utc_snoozed, reminder_date_user_snoozed
        if "nextweek_" in ack:
            reminder_date_user_snoozed = DatetimeUtils.add_weeks_to_datetime(user_reminder, 1)

            reminder_date_user_snoozed = DatetimeUtils.create_datetime(
                reminder_date_user_snoozed.year, reminder_date_user_snoozed.month, reminder_date_user_snoozed.day, 9, 0
            )

            reminder_date_utc_snoozed = DatetimeUtils.subtract_minutes_from_datetime(reminder_date_user_snoozed, offset)
            return reminder_date_utc_snoozed, reminder_date_user_snoozed
        if "nextmonth_" in ack:
            reminder_date_user_snoozed = DatetimeUtils.add_months_to_datetime(user_reminder, 1)

            reminder_date_user_snoozed = DatetimeUtils.create_datetime(
                reminder_date_user_snoozed.year, reminder_date_user_snoozed.month, reminder_date_user_snoozed.day, 9, 0
            )

            reminder_date_utc_snoozed = DatetimeUtils.subtract_minutes_from_datetime(reminder_date_user_snoozed, offset)
            return reminder_date_utc_snoozed, reminder_date_user_snoozed

    @staticmethod
    def snooze_reminder(customer_id: str, id: int, reminder_date_utc_snoozed, reminder_date_user_snoozed):
        reminder_date_utc_snoozed_str = DatetimeUtils.convert_datetime_to_string(reminder_date_utc_snoozed)
        reminder_date_user_snoozed_str = DatetimeUtils.convert_datetime_to_string(reminder_date_user_snoozed)
        RemindersRepo.snooze_reminder(customer_id, id, reminder_date_utc_snoozed_str, reminder_date_user_snoozed_str)
