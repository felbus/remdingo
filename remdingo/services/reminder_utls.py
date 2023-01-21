class ReminderUtils:
    @staticmethod
    def get_days_to_add(current_day_index, reminder_day_index):
        if reminder_day_index > current_day_index:
            # today is tuesday = 1 and want friday = 4, so need to add 3 days, so days_to_add = 4 - 1
            days_to_add = reminder_day_index - current_day_index
        elif reminder_day_index < current_day_index:
            # today is friday = 4 and want tuesday = 1 so need to add 4 days, so days_to_add = 7 - (4 - 1)
            days_to_add = 7 - (current_day_index - reminder_day_index)
        elif reminder_day_index == current_day_index:
            days_to_add = 7
        else:
            days_to_add = 0

        return days_to_add
