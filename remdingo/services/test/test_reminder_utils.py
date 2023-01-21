import unittest

from remdingo.services.reminder_utls import ReminderUtils


class TestReminderUtils(unittest.TestCase):
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
