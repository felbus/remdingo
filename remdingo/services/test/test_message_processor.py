import unittest
from datetime import date, time
import re

import pandas as pd
import pytz
from pytz import country_timezones

from remdingo.services.message_processor import MessageProcessor
from remdingo.utils.datetime_utils import DatetimeUtils
from remdingo.services.reminder_utls import ReminderUtils

from word2number import w2n


class TestMessageProcessor(unittest.TestCase):
    def test_can_detect_usa_timezone(self):
        gb = "Europe/London"
        x = MessageProcessor.is_usa_timezone(gb)
        self.assertEqual(False, x)

        us = "America/Los_Angeles"
        x = MessageProcessor.is_usa_timezone(us)
        self.assertEqual(True, x)

    def test_can_detect_full_d_m_y_t_regex(self):
        message = "on 1/2/2019 12:34:54 do something cool"
        dmy = MessageProcessor.regex_detect_full_d_m_y_t_with_seconds(message)
        self.assertEqual(True, dmy)

    def test_get_days_to_add_1(self):
        # sunday to monday = 1 day
        current_day_index = 6
        reminder_day_index = 0
        days_to_add = ReminderUtils.get_days_to_add(current_day_index, reminder_day_index)
        self.assertEqual(1, days_to_add)

    def test_get_days_to_add_2(self):
        # weds to fri = 2 day
        current_day_index = 2
        reminder_day_index = 4
        days_to_add = ReminderUtils.get_days_to_add(current_day_index, reminder_day_index)
        self.assertEqual(2, days_to_add)

    def test_get_days_to_add_3(self):
        # weds to mon = 5 day
        current_day_index = 2
        reminder_day_index = 0
        days_to_add = ReminderUtils.get_days_to_add(current_day_index, reminder_day_index)
        self.assertEqual(5, days_to_add)

    def test_get_days_to_add_4(self):
        # sun to fri = 5 day
        current_day_index = 6
        reminder_day_index = 4
        days_to_add = ReminderUtils.get_days_to_add(current_day_index, reminder_day_index)
        self.assertEqual(5, days_to_add)

    def test_can_detect_dmy_regex(self):
        message_components = "at 12:34 on 1/2/2022".split(" ")
        dmy = MessageProcessor.check_for_dmy_date_format(message_components)
        self.assertEqual((True, 3, "/"), dmy)

        message_components = "at 12:34 on 11/12/2022".split(" ")
        dmy = MessageProcessor.check_for_dmy_date_format(message_components)
        self.assertEqual((True, 3, "/"), dmy)

        message_components = "at 12:34 on 30/03/2022".split(" ")
        dmy = MessageProcessor.check_for_dmy_date_format(message_components)
        self.assertEqual((True, 3, "/"), dmy)

    def test_can_detect_dm_regex(self):
        message_components = "at 12:34 on 1/2".split(" ")
        dmy = MessageProcessor.check_for_dm_date_format(message_components)
        self.assertEqual((True, 3, "/"), dmy)

        message_components = "at 12:34 on 11/12".split(" ")
        dmy = MessageProcessor.check_for_dm_date_format(message_components)
        self.assertEqual((True, 3, "/"), dmy)

        message_components = "at 12:34 on 30/03".split(" ")
        dmy = MessageProcessor.check_for_dm_date_format(message_components)
        self.assertEqual((True, 3, "/"), dmy)

    def test_can_detect_first_time_period_location(self):
        message_components = "in one hour do something".split(" ")
        first_time_period_location = MessageProcessor.get_time_period_location(message_components, 1)
        self.assertEqual(2, first_time_period_location)

        message_components = "in thirty one days do something".split(" ")
        first_time_period_location = MessageProcessor.get_time_period_location(message_components, 1)
        self.assertEqual(3, first_time_period_location)

        message_components = "in 5 hrs and one days do something".split(" ")
        first_time_period_location = MessageProcessor.get_time_period_location(message_components, 1)
        self.assertEqual(2, first_time_period_location)

        message_components = "in three hundred wks and one days do something".split(" ")
        first_time_period_location = MessageProcessor.get_time_period_location(message_components, 1)
        self.assertEqual(3, first_time_period_location)

    def test_can_detect_second_time_period_location(self):
        message_components = "in one hour and 30 mins do something".split(" ")
        second_time_period_location = MessageProcessor.get_time_period_location(message_components, 2)
        self.assertEqual(5, second_time_period_location)

    def test_can_detect_month_location(self):
        message_components = "at 1645 on march 10th do something".split(" ")
        month_location = MessageProcessor.get_month_location(message_components)
        self.assertEqual(3, month_location)

    def test_can_count_time_periods(self):
        message_components = "in one hour and 30 mins do something".split(" ")
        tps = MessageProcessor.count_number_of_time_periods(message_components)
        self.assertEqual(2, tps)

        message_components = "in one day".split(" ")
        tps = MessageProcessor.count_number_of_time_periods(message_components)
        self.assertEqual(1, tps)

        message_components = "in three days two hours and 30 mins do something".split(" ")
        tps = MessageProcessor.count_number_of_time_periods(message_components)
        self.assertEqual(3, tps)

    def test_can_turn_string_number_to_int(self):
        message_components = "in thirty two hours do something".split(" ")
        time_period_location = 3

        number_str = " ".join(message_components[1:time_period_location])
        number = w2n.word_to_num(number_str)

        self.assertEqual(32, number)

    def test_can_get_first_time_element(self):
        message_components = "in thirty two hours do something".split(" ")
        time_element_occurrence = 1
        start_position = 1
        time_period_location, time_period, number = MessageProcessor.get_time_element(message_components, time_element_occurrence, start_position)

        self.assertEqual(3, time_period_location)
        self.assertEqual("hours", time_period)
        self.assertEqual(32, number)

        message_components = "in 42 mins do something".split(" ")
        time_element_occurrence = 1
        start_position = 1
        time_period_location, time_period, number = MessageProcessor.get_time_element(message_components, time_element_occurrence, start_position)

        self.assertEqual(2, time_period_location)
        self.assertEqual("mins", time_period)
        self.assertEqual(42, number)

    def test_can_get_second_time_element(self):
        message_components = "in thirty two hours and five minutes do something".split(" ")
        time_element_occurrence = 2
        start_position = 4
        time_period_location, time_period, number = MessageProcessor.get_time_element(message_components, time_element_occurrence, start_position)

        self.assertEqual(6, time_period_location)
        self.assertEqual("minutes", time_period)
        self.assertEqual(5, number)

        message_components = "in thirty two hours five minutes do something".split(" ")
        time_element_occurrence = 2
        start_position = 4
        time_period_location, time_period, number = MessageProcessor.get_time_element(message_components, time_element_occurrence, start_position)

        self.assertEqual(5, time_period_location)
        self.assertEqual("minutes", time_period)
        self.assertEqual(5, number)

    def test_get_time_from_string_colon(self):
        t = MessageProcessor.get_time_from_string("11:58")
        self.assertEqual(time(11, 58), t)

    def test_can_get_time_from_string(self):
        time_str = "0912"
        t = MessageProcessor.get_time_from_string(time_str)
        self.assertEqual(time(9, 12), t)

        time_str = "1742"
        t = MessageProcessor.get_time_from_string(time_str)
        self.assertEqual(time(17, 42), t)

        time_str = "10:15"
        t = MessageProcessor.get_time_from_string(time_str)
        self.assertEqual(time(10, 15), t)

        time_str = "1:35"
        t = MessageProcessor.get_time_from_string(time_str)
        self.assertEqual(time(1, 35), t)

        time_str = "23:45"
        t = MessageProcessor.get_time_from_string(time_str)
        self.assertEqual(time(23, 45), t)

        time_str = "23:45pm"
        t = MessageProcessor.get_time_from_string(time_str)
        self.assertEqual(time(23, 45), t)

        time_str = "9:47am"
        t = MessageProcessor.get_time_from_string(time_str)
        self.assertEqual(time(9, 47), t)

        time_str = "9:49pm"
        t = MessageProcessor.get_time_from_string(time_str)
        self.assertEqual(time(21, 49), t)

        time_str = "11:49pm"
        t = MessageProcessor.get_time_from_string(time_str)
        self.assertEqual(time(23, 49), t)

    def test_can_get_time_from_string_11(self):
        time_str = "6am"
        t = MessageProcessor.get_time_from_string(time_str)
        self.assertEqual(time(6, 0), t)

    def test_can_get_time_from_string_1(self):
        time_str = "3pm"
        t = MessageProcessor.get_time_from_string(time_str)
        self.assertEqual(time(15, 0), t)

    def test_can_detect_valid_time_format_12_hour(self):
        result = MessageProcessor.check_for_time_format(["01:12AM"])
        self.assertEqual(True, result[0])
        result = MessageProcessor.check_for_time_format(["01:12PM"])
        self.assertEqual(True, result[0])
        result = MessageProcessor.check_for_time_format(["34:12PM"])
        self.assertEqual(False, result[0])
        result = MessageProcessor.check_for_time_format(["18:12AM"])
        self.assertEqual(True, result[0])

    def test_can_detect_valid_time_format_24_hour_no_colon(self):
        result = MessageProcessor.check_for_time_format(["1812"])
        self.assertEqual(True, result[0])

        result = MessageProcessor.check_for_time_format(["18:12"])
        self.assertEqual(True, result[0])

    def test_can_detect_valid_time_format_24_hour(self):
        result = MessageProcessor.check_for_time_format(["9:12"])
        self.assertEqual(True, result[0])
        result = MessageProcessor.check_for_time_format(["56:12"])
        self.assertEqual(False, result[0])
        result = MessageProcessor.check_for_time_format(["25:12"])
        self.assertEqual(False, result[0])
        result = MessageProcessor.check_for_time_format(["01:12"])
        self.assertEqual(True, result[0])

    def test_can_detect_valid_time_format2(self):
        result = MessageProcessor.check_for_time_format(["1PM"])
        self.assertEqual(True, result[0])
        result = MessageProcessor.check_for_time_format(["3PM"])
        self.assertEqual(True, result[0])
        result = MessageProcessor.check_for_time_format(["11PM"])
        self.assertEqual(True, result[0])
        result = MessageProcessor.check_for_time_format(["11 PM"])
        self.assertEqual(False, result[0])
        result = MessageProcessor.check_for_time_format(["PM"])
        self.assertEqual(False, result[0])
        result = MessageProcessor.check_for_time_format(["21PM"])
        self.assertEqual(False, result[0])
        result = MessageProcessor.check_for_time_format(["13PM"])
        self.assertEqual(False, result[0])

    def test_can_extract_month_day_year_1(self):
        base_dt = DatetimeUtils.create_datetime(2021, 1, 1, 14, 15)

        message_components = "at 1645 on march 10th do something".split(" ")
        correct_dt = DatetimeUtils.create_date(2021, 3, 10)
        dt = MessageProcessor.extract_month_day_year(message_components, 3, base_dt)
        self.assertEqual((correct_dt, 5), dt)

        message_components = "at 1645 on march 10 do something".split(" ")
        correct_dt = DatetimeUtils.create_date(2021, 3, 10)
        dt = MessageProcessor.extract_month_day_year(message_components, 3, base_dt)
        self.assertEqual((correct_dt, 5), dt)

    def test_can_extract_month_day_year_2(self):
        message_components = "at 1645 on march 22nd 2022 do something".split(" ")
        correct_dt = DatetimeUtils.create_date(2022, 3, 22)
        dt = MessageProcessor.extract_month_day_year(message_components, 3)
        self.assertEqual((correct_dt, 6), dt)

        message_components = "at 1645 on march 10 2022 do something".split(" ")
        correct_dt = DatetimeUtils.create_date(2022, 3, 10)
        dt = MessageProcessor.extract_month_day_year(message_components, 3)
        self.assertEqual((correct_dt, 6), dt)