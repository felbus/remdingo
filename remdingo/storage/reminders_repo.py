import pandas as pd
from sqlalchemy import text
from typing import Dict

from remdingo.storage.postgres_connector import DbConnector

remdingo_engine = DbConnector.get_remdingo_engine()


class RemindersRepo:
    def __init__(self):
        pass

    @staticmethod
    def run_pandas_query(sql: str, params: dict = None) -> pd.DataFrame:
        try:
            if params:
                return pd.read_sql_query(text(sql), remdingo_engine, params=params)
            return pd.read_sql_query(text(sql), remdingo_engine)
        except Exception as e:
            raise e

    @staticmethod
    def save_reminder(customer_id: str, reminder_date_utc: str, reminder_date_user: str, message: str, created: str, offset: int, tz: str):
        sql = """
            INSERT INTO remdingodb.public.reminders(customer_id, reminder_date_utc, reminder_date_user, reminder_text, snooze_number, ack, sms, email, web, "offset", tz, created)
            VALUES (:customer_id, :reminder_date_utc, :reminder_date_user, :message, 0, False, False, False, False, :offset, :tz, :created)
        """
        params = {
            'customer_id': customer_id,
            'reminder_date_utc': reminder_date_utc,
            'reminder_date_user': reminder_date_user,
            'message': message,
            'offset': offset,
            'tz': tz,
            'created': created
        }
        return DbConnector.execute_query(remdingo_engine, sql, params)

    @staticmethod
    def snooze_reminder(customer_id: str, id: int, reminder_date_utc: str, reminder_date_user: str):
        sql = """
            UPDATE remdingodb.public.reminders
            SET reminder_date_utc = :reminder_date_utc, reminder_date_user = :reminder_date_user
            WHERE id = :id AND customer_id = :customer_id
        """
        params = {
            'reminder_date_utc': reminder_date_utc,
            'reminder_date_user': reminder_date_user,
            'id': id,
            'customer_id': customer_id
        }
        return DbConnector.execute_query(remdingo_engine, sql, params)

    @staticmethod
    def ack_reminder(customer_id: str, id: int):
        sql = "UPDATE remdingodb.public.reminders SET ack = True WHERE id = :id AND customer_id = :customer_id"
        params = {'id': id, 'customer_id': customer_id}
        return DbConnector.execute_query(remdingo_engine, sql, params)

    @staticmethod
    def get_reminder(customer_id: str, id: int):
        sql = "SELECT * FROM remdingodb.public.reminders WHERE id = :id AND customer_id = :customer_id"
        params = {'id': id, 'customer_id': customer_id}
        return pd.read_sql_query(text(sql), remdingo_engine, params=params)

    @staticmethod
    def check_reminders(customer_id):
        sql = """
            SELECT * FROM remdingodb.public.reminders
            WHERE customer_id = :customer_id AND ack = False AND reminder_date_utc <= now() at time zone 'utc'
        """
        params = {'customer_id': customer_id}
        return RemindersRepo.run_pandas_query(sql, params)

    @staticmethod
    def get_all_reminders(customer_id):
        sql = "SELECT * FROM remdingodb.public.reminders WHERE customer_id = :customer_id AND ack = False ORDER BY reminder_date_utc ASC"
        params = {'customer_id': customer_id}
        return RemindersRepo.run_pandas_query(sql, params)

    @staticmethod
    def get_reminders_history(customer_id):
        sql = "SELECT * FROM remdingodb.public.reminders WHERE customer_id = :customer_id ORDER BY reminder_date_utc DESC LIMIT 50"
        params = {'customer_id': customer_id}
        return RemindersRepo.run_pandas_query(sql, params)
