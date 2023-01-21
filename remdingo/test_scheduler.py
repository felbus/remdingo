import uuid
import time

from remdingo.utils.datetime_utils import DatetimeUtils

"""
from apscheduler.schedulers.background import BackgroundScheduler
from remdingo.app.services.message_processor import MessageProcessor

scheduler = BackgroundScheduler()
scheduler.start()


def sensor(s: str):
    print(f"Scheduler is alive! {s}")


if __name__ == '__main__':

    now = DatetimeUtils.get_local_datetime()
    now_plus_1 = DatetimeUtils.add_minutes_to_datetime(now, 1)
    now_plus_2 = DatetimeUtils.add_minutes_to_datetime(now, 2)
    print(now)
    print(now_plus_1)

    scheduler.add_job(sensor, 'date', run_date=now_plus_1, id=str(uuid.uuid4()), args=['boom this is a parameter'])

    while DatetimeUtils.get_local_datetime() < now_plus_2:
        print(f"time is now {DatetimeUtils.get_local_datetime()} waiting for schedule at {now_plus_1} sleeping for 20 seconds")
        time.sleep(20)
"""