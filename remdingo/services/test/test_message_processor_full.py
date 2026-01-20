import unittest
from datetime import date, time

from remdingo.services.message_processor import MessageProcessor
from remdingo.utils.datetime_utils import DatetimeUtils
from remdingo.storage.reminders_repo import RemindersRepo
from remdingo.services.reminders_check import RemindersCheck

import pandas as pd
from word2number import w2n


class TestMessageProcessor(unittest.TestCase):
    def test_can_snooze_reminder(self):
        ack = "15mins_"
        offset = 60

        input_reminder_date_utc = DatetimeUtils.create_datetime(2021, 7, 17, 9, 8)
        input_reminder_date_user = DatetimeUtils.create_datetime(2021, 7, 17, 10, 8)
        correct_result_reminder_date_utc = DatetimeUtils.create_datetime(2021, 7, 17, 9, 23)
        correct_result_reminder_date_user = DatetimeUtils.create_datetime(2021, 7, 17, 10, 23)

        data = [[input_reminder_date_utc, input_reminder_date_user]]
        r = pd.DataFrame(data, columns=['reminder_date_utc', 'reminder_date_user'])

        result_reminder_date_utc, result_reminder_date_user = RemindersCheck.process_reminder_snooze(ack, offset, input_reminder_date_utc)

        self.assertEqual(correct_result_reminder_date_utc, result_reminder_date_utc)
        self.assertEqual(correct_result_reminder_date_user, result_reminder_date_user)

    def test_can_process_message_1w111(self):
        offset = 0
        message = "9am intro to bi"
        base_dt = DatetimeUtils.create_datetime(2022, 1, 5, 18, 49)
        result_dt = DatetimeUtils.create_datetime(2022, 1, 6, 9, 0)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("intro to bi", message_str)

        offset = 0
        message = "1800 intro to bi"
        base_dt = DatetimeUtils.create_datetime(2022, 1, 5, 18, 49)
        result_dt = DatetimeUtils.create_datetime(2022, 1, 6, 18, 0)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("intro to bi", message_str)

        offset = 0
        message = "2000 intro to bi"
        base_dt = DatetimeUtils.create_datetime(2022, 1, 5, 18, 49)
        result_dt = DatetimeUtils.create_datetime(2022, 1, 5, 20, 0)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("intro to bi", message_str)

    def test_can_process_message_1111(self):
        offset = 0
        message = "monday intro to bi"
        base_dt = DatetimeUtils.create_datetime(2022, 1, 5, 18, 49)
        result_dt = DatetimeUtils.create_datetime(2022, 1, 10, 9, 0)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("intro to bi", message_str)

    def test_can_process_message_1_min(self):
        offset = 0
        message = "in one min go shopping"
        base_dt = DatetimeUtils.create_datetime(2021, 7, 17, 9, 8)
        result_dt = DatetimeUtils.create_datetime(2021, 7, 17, 9, 9)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("go shopping", message_str)

    def test_can_process_message_1(self):
        offset = 0
        message = "in one hour go shopping"
        base_dt = DatetimeUtils.create_datetime(2021, 7, 17, 9, 8)
        result_dt = DatetimeUtils.create_datetime(2021, 7, 17, 10, 8)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("go shopping", message_str)

        message = "in 1 hour go shopping"
        result_dt = DatetimeUtils.create_datetime(2021, 7, 17, 10, 8)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("go shopping", message_str)

        message = "in 1 hr go shopping"
        result_dt = DatetimeUtils.create_datetime(2021, 7, 17, 10, 8)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("go shopping", message_str)

    def test_can_process_message_2(self):
        offset = 0
        message = "in one hour and 30 mins go shopping"
        base_dt = DatetimeUtils.create_datetime(2021, 7, 17, 9, 8)
        result_dt = DatetimeUtils.create_datetime(2021, 7, 17, 10, 38)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("go shopping", message_str)

        message = "in 1 hour and thirty two minutes go shopping"
        result_dt = DatetimeUtils.create_datetime(2021, 7, 17, 10, 40)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("go shopping", message_str)

        message = "in 2 hours and 32 minutes go shopping"
        result_dt = DatetimeUtils.create_datetime(2021, 7, 17, 11, 40)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("go shopping", message_str)

        message = "in 2 hours 32 minutes go shopping"
        result_dt = DatetimeUtils.create_datetime(2021, 7, 17, 11, 40)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("go shopping", message_str)

        message = "in 2 hrs 32 minutes go shopping"
        result_dt = DatetimeUtils.create_datetime(2021, 7, 17, 11, 40)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("go shopping", message_str)

    def test_can_process_message_3(self):
        offset = 60
        message = "in 2 weeks 22 hours and 35 minutes do a poo"
        base_dt = DatetimeUtils.create_datetime(2021, 7, 17, 9, 8)
        result_dt = DatetimeUtils.create_datetime(2021, 8, 1, 8, 43)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_user)
        self.assertEqual("do a poo", message_str)

    def test_can_process_message_4(self):
        offset = 0
        message = "at 1645 do a poo"
        base_dt = DatetimeUtils.create_datetime(2021, 7, 17, 9, 8)
        result_dt = DatetimeUtils.create_datetime(2021, 7, 17, 16, 45)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("do a poo", message_str)

    def test_can_process_message_41(self):
        offset = 0
        message = "at 6:00am do a poo"
        base_dt = DatetimeUtils.create_datetime(2021, 7, 17, 4, 8)
        result_dt = DatetimeUtils.create_datetime(2021, 7, 17, 6, 0)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("do a poo", message_str)

    def test_can_process_message_42(self):
        offset = 0
        message = "at 6am do a poo"
        base_dt = DatetimeUtils.create_datetime(2021, 7, 17, 3, 8)
        result_dt = DatetimeUtils.create_datetime(2021, 7, 17, 6, 0)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("do a poo", message_str)

    def test_can_process_message_5(self):
        offset = 0
        message = "at 17:37 on 5th oct 2022 do a poo"
        base_dt = DatetimeUtils.create_datetime(2022, 9, 1, 10, 0)
        result_dt = DatetimeUtils.create_datetime(2022, 10, 5, 17, 37)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("do a poo", message_str)

    def test_can_process_message_6(self):
        offset = 0
        message = "at 17:37 on 5th jan do a poo"
        base_dt = DatetimeUtils.create_datetime(2021, 12, 17, 14, 15)
        result_dt = DatetimeUtils.create_datetime(2022, 1, 5, 17, 37)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("do a poo", message_str)

    def test_can_process_message_7(self):
        offset = 0
        message = "at 17:37 5th jan do a poo"
        base_dt = DatetimeUtils.create_datetime(2021, 12, 17, 14, 15)
        result_dt = DatetimeUtils.create_datetime(2022, 1, 5, 17, 37)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("do a poo", message_str)

    def test_can_process_message_9(self):
        offset = 0
        message = "at 19:48 jan 5 do a poo"
        base_dt = DatetimeUtils.create_datetime(2021, 12, 17, 14, 15)
        result_dt = DatetimeUtils.create_datetime(2022, 1, 5, 19, 48)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("do a poo", message_str)

    def test_can_process_message_8(self):
        offset = 0
        tz = "Europe/London"
        message = "at 17:37 on 15/7 do a poo"
        base_dt = DatetimeUtils.create_datetime(2021, 5, 29, 14, 15)
        result_dt = DatetimeUtils.create_datetime(2021, 7, 15, 17, 37)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, tz=tz, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("do a poo", message_str)

        offset = 0
        tz = "Europe/London"
        message = "at 17:37 on 15/7/2022 do a poo"
        base_dt = DatetimeUtils.create_datetime(2021, 5, 29, 14, 15)
        result_dt = DatetimeUtils.create_datetime(2022, 7, 15, 17, 37)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, tz=tz, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("do a poo", message_str)

    def test_can_process_message_81(self):
        offset = 0
        tz = "America/Los_Angeles"
        message = "at 17:37 on 7/15 do a poo"
        base_dt = DatetimeUtils.create_datetime(2021, 5, 29, 14, 15)
        result_dt = DatetimeUtils.create_datetime(2021, 7, 15, 17, 37)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, tz=tz, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("do a poo", message_str)

        offset = 0
        tz = "America/Los_Angeles"
        message = "at 17:37 on 7/15/2022 do a poo"
        base_dt = DatetimeUtils.create_datetime(2021, 5, 29, 14, 15)
        result_dt = DatetimeUtils.create_datetime(2022, 7, 15, 17, 37)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, tz=tz, base_dt=base_dt)

        self.assertEqual(success, True)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("do a poo", message_str)

    def test_can_process_message_82(self):
        offset = 0
        tz = "America/Los_Angeles"
        message = "at 11:37 do a poo"
        base_dt = DatetimeUtils.create_datetime(2021, 5, 29, 14, 15)
        result_dt = DatetimeUtils.create_datetime(2021, 5, 29, 11, 37)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, tz=tz, base_dt=base_dt)

        self.assertEqual(success, False)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("reminder is in the past", message_str)

    def test_can_process_message_82(self):
        offset = 0
        tz = "America/Los_Angeles"
        message = "at 11:37 do a poo"
        base_dt = DatetimeUtils.create_datetime(2021, 5, 29, 14, 15)
        result_dt = DatetimeUtils.create_datetime(2021, 5, 29, 11, 37)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, tz=tz, base_dt=base_dt)

        self.assertEqual(success, False)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("reminder is in the past", message_str)

    def test_can_process_message_92(self):
        offset = 240
        tz = "America/Los_Angeles"
        message = "at 11 do a poo"
        base_dt = DatetimeUtils.create_datetime(2021, 7, 28, 6, 8)
        result_dt = DatetimeUtils.create_datetime(2021, 7, 28, 11, 0)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, tz=tz, base_dt=base_dt)

        self.assertEqual(True, success)
        self.assertEqual(result_dt, reminder_date_user)

    def test_can_process_message_yesterdday(self):
        offset = 240
        tz = "America/Los_Angeles"
        message = "yesterday at 11 do a poo"
        base_dt = DatetimeUtils.create_datetime(2021, 7, 28, 6, 8)
        result_dt = DatetimeUtils.create_datetime(2021, 7, 28, 11, 0)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, tz=tz, base_dt=base_dt)

        self.assertEqual(False, success)
        self.assertEqual("cannot set reminders in the past", message_str)

    def test_can_process_message_fail(self):
        offset = 240
        tz = "America/Los_Angeles"
        message = "dfdf fwwf wrf"
        base_dt = DatetimeUtils.create_datetime(2021, 7, 28, 6, 8)
        result_dt = DatetimeUtils.create_datetime(2021, 7, 28, 11, 0)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, tz=tz, base_dt=base_dt)

        self.assertEqual(False, success)
        self.assertEqual("", message_str)

    def test_can_process_message_tomorrow_1(self):
        offset = 240
        tz = "America/Los_Angeles"
        message = "tomorrow at 1136 pick up delivery"
        base_dt = DatetimeUtils.create_datetime(2021, 7, 28, 6, 8)
        result_dt = DatetimeUtils.create_datetime(2021, 7, 29, 11, 36)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, tz=tz, base_dt=base_dt)

        self.assertEqual(True, success)
        self.assertEqual(result_dt, reminder_date_user)

    def test_can_process_message_tomorrow(self):
        offset = 240
        tz = "America/Los_Angeles"
        message = "tomorrow pick up delivery"
        base_dt = DatetimeUtils.create_datetime(2021, 7, 28, 6, 8)
        result_dt = DatetimeUtils.create_datetime(2021, 7, 29, 9, 0)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, tz=tz, base_dt=base_dt)

        self.assertEqual(True, success)
        self.assertEqual(result_dt, reminder_date_user)

    def test_can_process_message_dow_1(self):
        offset = 240
        tz = "America/Los_Angeles"
        message = "thursday at 11:58 pick up delivery"
        base_dt = DatetimeUtils.create_datetime(2021, 12, 28, 9, 10)
        result_dt = DatetimeUtils.create_datetime(2021, 12, 30, 11, 58)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, tz=tz, base_dt=base_dt)

        self.assertEqual(True, success)
        self.assertEqual(result_dt, reminder_date_user)

        message = "sunday pick up delivery"
        base_dt = DatetimeUtils.create_datetime(2021, 12, 28, 9, 10)
        result_dt = DatetimeUtils.create_datetime(2022, 1, 2, 9, 0)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, tz=tz, base_dt=base_dt)

        self.assertEqual(True, success)
        self.assertEqual(result_dt, reminder_date_user)

    def test_can_process_message_dow_2(self):
        offset = 240
        tz = "America/Los_Angeles"
        message = "next thursday at 11:58 pick up delivery"
        base_dt = DatetimeUtils.create_datetime(2021, 12, 7, 9, 10)
        result_dt = DatetimeUtils.create_datetime(2021, 12, 16, 11, 58)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, tz=tz, base_dt=base_dt)

        self.assertEqual(True, success)
        self.assertEqual(result_dt, reminder_date_user)

    def test_can_process_message_with_comma_after_time_period(self):
        """Test that punctuation after time periods (e.g., 'minutes,') is handled correctly."""
        offset = 0
        message = "in five minutes, take the dog out"
        base_dt = DatetimeUtils.create_datetime(2021, 7, 17, 9, 8)
        result_dt = DatetimeUtils.create_datetime(2021, 7, 17, 9, 13)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(True, success)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("take the dog out", message_str)

    def test_can_process_message_tomorrow_with_comma(self):
        """Test that 'Tomorrow,' with a comma is handled correctly."""
        offset = 0
        message = "Tomorrow, remind me about Ricky's augment survey."
        base_dt = DatetimeUtils.create_datetime(2021, 7, 17, 9, 8)
        result_dt = DatetimeUtils.create_datetime(2021, 7, 18, 9, 0)
        reminder_date_utc, reminder_date_user, message_str, success = MessageProcessor.process_message(message, offset, base_dt=base_dt)

        self.assertEqual(True, success)
        self.assertEqual(result_dt, reminder_date_utc)
        self.assertEqual("remind me about ricky's augment survey", message_str)