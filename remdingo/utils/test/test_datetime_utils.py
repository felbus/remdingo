import unittest
from datetime import date, time, datetime
import time

from remdingo.utils.datetime_utils import DatetimeUtils


class TestDateTimeUtils(unittest.TestCase):
    def test_can_get_utc(self):
        x = DatetimeUtils.get_current_utc()
        print(x)

    def test_can_remove_micro_seconds_from_string(self):
        date_str = "2020-02-23 22:33:56.146715"
        d = DatetimeUtils.convert_string_to_datetime(date_str)
        dnm = d.replace(microsecond=0)
        s = DatetimeUtils.convert_datetime_to_string(dnm).replace(".000000", "")
        self.assertTrue(s == "2020-02-23 22:33:56")

    def test_can_get_current_date_hour(self):
        x = DatetimeUtils.get_current_utc()
        x = x.replace(minute=0, second=0, microsecond=0)
        x = DatetimeUtils.convert_datetime_to_string(x)

    def test_can_convert_str_date_to_datetime(self):
        x = DatetimeUtils.convert_string_to_datetime("2019-08-01 00:00:00")
        self.assertEqual(type(x), datetime)

    def test_epoch_conversion_from_datetime(self):
        epoch = DatetimeUtils.epoch_from_datetime_str("2019-08-01 14:32:56")
        self.assertEqual(epoch, 1564669976)

    def test_epoch_conversion_from_date(self):
        epoch = DatetimeUtils.epoch_from_date_str("2019-08-01")
        self.assertEqual(epoch, 1564617600)

    def test_datetime_conversion_from_epoch(self):
        d = DatetimeUtils.datetime_from_epoch(1564666376)
        self.assertEqual(d, DatetimeUtils.convert_string_to_datetime("2019-08-01 13:32:56"))

    def test_date_conversion_from_epoch(self):
        d = DatetimeUtils.date_from_epoch(1564614000)
        if time.tzname == ('GMT', 'BST'):
            self.assertEqual(d, DatetimeUtils.convert_string_to_date("2019-08-01"))
        else:
            self.assertEqual(d, DatetimeUtils.convert_string_to_date("2019-07-31"))

    def test_can_get_days_between_dates(self):
        min_date = DatetimeUtils.convert_string_to_datetime("2019-12-24 07:04:55.566176")
        max_date = DatetimeUtils.convert_string_to_datetime("2019-12-20 07:03:33.564558")
        days = DatetimeUtils.get_days_difference_between_dates(min_date, max_date, True)
        self.assertEqual(5, days)

    def test_can_get_days_between_dates_over_a_month(self):
        min_date = DatetimeUtils.convert_string_to_datetime("2019-06-24 07:04:55.566176")
        max_date = DatetimeUtils.convert_string_to_datetime("2019-09-20 07:03:33.564558")
        days = DatetimeUtils.get_days_difference_between_dates(min_date, max_date, True)
        self.assertEqual(89, days)

    def test_can_get_days_between_dates_over_a_year(self):
        min_date = DatetimeUtils.convert_string_to_datetime("2017-06-24 07:04:55.566176")
        max_date = DatetimeUtils.convert_string_to_datetime("2019-09-20 07:03:33.564558")
        days = DatetimeUtils.get_days_difference_between_dates(min_date, max_date, True)
        self.assertEqual(819, days)

    def test_is_date_or_datetime(self):
        d = DatetimeUtils.convert_string_to_datetime("2019-12-24 07:04:55.566176")
        self.assertTrue(DatetimeUtils.is_date_or_datetime(d))

        d = DatetimeUtils.convert_string_to_datetime("2019-12-23")
        self.assertTrue(DatetimeUtils.is_date_or_datetime(d.date()))

    def test_can_convert_to_date_and_back_to_string(self):
        date_str = "2019-08-05"
        dt = DatetimeUtils.convert_string_to_datetime(date_str)
        ds = DatetimeUtils.convert_date_to_string(dt)
        self.assertEqual(date_str, ds)

    def test_can_convert_str_date_to_date(self):
        x = DatetimeUtils.convert_string_to_datetime("2019-08-01")
        self.assertEqual(type(x), datetime)

    def test_can_get_seconds_between_datetime(self):
        start = DatetimeUtils.get_backwards_datetime(5)
        end = DatetimeUtils.add_seconds_to_datetime(start, 400)
        time_taken = DatetimeUtils.get_seconds_difference_between_dates(start, end)
        self.assertEqual(400, time_taken)

        start = DatetimeUtils.get_backwards_datetime(0)
        end = DatetimeUtils.add_seconds_to_datetime(start, 4338542)
        time_taken = DatetimeUtils.get_seconds_difference_between_dates(start, end)
        self.assertEqual(4338542, time_taken)

    def test_can_sort_list_of_dates(self):
        str_dates = ['2018-01-09', '2018-01-10', '2018-01-11', '2018-01-12', '2018-01-08 13:00:00', '2018-01-13', '2018-01-08 08:00:00', '2018-01-14', '2018-01-15']
        safe_dates = DatetimeUtils.build_datetime_list(str_dates)
        self.assertEqual(safe_dates[0], DatetimeUtils.convert_string_to_datetime('2018-01-08 08:00:00'))

    def test_can_get_min_max_diff(self):
        str_dates = ['2018-01-09', '2018-01-10', '2018-01-11', '2018-01-12', '2018-01-08 13:00:00', '2018-01-13', '2018-01-08 08:00:00', '2018-01-15', '2018-01-14']
        safe_dates = DatetimeUtils.build_datetime_list(str_dates)
        min_date, max_date, diff_dates = DatetimeUtils.get_min_max_diff(safe_dates)
        self.assertEqual(min_date, DatetimeUtils.convert_string_to_datetime('2018-01-08 08:00:00'))
        self.assertEqual(max_date, DatetimeUtils.convert_string_to_datetime('2018-01-15'))
        self.assertEqual(diff_dates, 8)

    def test_can_subtract_months_from_date_with_lower_max_date(self):
        r = DatetimeUtils.subtract_months_from_date(DatetimeUtils.convert_string_to_date("2019-12-31"), 3)
        self.assertEqual(r, DatetimeUtils.convert_string_to_date("2019-09-30"))

        r = DatetimeUtils.subtract_months_from_date(DatetimeUtils.convert_string_to_date("2019-03-31"), 1)
        self.assertEqual(r, DatetimeUtils.convert_string_to_date("2019-02-28"))

    def test_can_subtract_months_from_date_with_day_in_range(self):
        r = DatetimeUtils.subtract_months_from_date(DatetimeUtils.convert_string_to_date("2019-03-15"), 1)
        self.assertEqual(r, DatetimeUtils.convert_string_to_date("2019-02-15"))

    def test_can_convert_string_to_datetime(self):
        d = DatetimeUtils.convert_string_to_datetime("2019-05-29")
        self.assertTrue(type(d) == datetime)


if __name__ == '__main__':
    unittest.main()
