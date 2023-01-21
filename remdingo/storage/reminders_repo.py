import pandas as pd
from typing import Dict

from remdingo.storage.postgres_connector import DbConnector

remdingo_engine = DbConnector.get_remdingo_engine()


class RemindersRepo:
    def __init__(self):
        pass

    @staticmethod
    def run_pandas_query(sql: str) -> pd.DataFrame:
        try:
            return pd.read_sql_query(sql, remdingo_engine)
        except Exception as e:
            raise e

    @staticmethod
    def save_reminder(customer_id: str, reminder_date_utc: str, reminder_date_user: str, message: str, created: str, offset: int, tz: str):
        sql = f"""
            insert into remdingodb.public.reminders(customer_id, reminder_date_utc, reminder_date_user, reminder_text, snooze_number, ack, sms, email, web, "offset", tz, created)  
            values ('{customer_id}', '{reminder_date_utc}', '{reminder_date_user}', '{message}', 0, 'False', 'False', 'False', 'False', {offset}, '{tz}', '{created}');            
        """
        return DbConnector.execute_query(remdingo_engine, sql)

    @staticmethod
    def snooze_reminder(customer_id: str, id: int, reminder_date_utc: str, reminder_date_user: str):
        sql = f"""
            update remdingodb.public.reminders 
            set  reminder_date_utc = '{reminder_date_utc}', reminder_date_user = '{reminder_date_user}'
            where id = {id} and customer_id = '{customer_id}';
        """
        return DbConnector.execute_query(remdingo_engine, sql)

    @staticmethod
    def ack_reminder(customer_id: str, id: int):
        sql = f"update remdingodb.public.reminders set ack = 'True' where id = {id} and customer_id = '{customer_id}';"
        return DbConnector.execute_query(remdingo_engine, sql)

    @staticmethod
    def get_reminder(customer_id: str, id: int):
        sql = f"select * from remdingodb.public.reminders where id = {id} and customer_id = '{customer_id}';"
        return pd.read_sql_query(sql, remdingo_engine)

    @staticmethod
    def check_reminders(customer_id):
        sql = f"""
            select * from remdingodb.public.reminders 
            where customer_id = '{customer_id}' and ack = False and reminder_date_utc <= now() at time zone 'utc';
        """
        return RemindersRepo.run_pandas_query(sql)

    @staticmethod
    def get_all_reminders(customer_id):
        sql = f"select * from remdingodb.public.reminders where customer_id = '{customer_id}' and ack = False order by reminder_date_utc asc"
        return RemindersRepo.run_pandas_query(sql)

    @staticmethod
    def get_reminders_history(customer_id):
        sql = f"select * from remdingodb.public.reminders where customer_id = '{customer_id}' order by reminder_date_utc desc limit 50;"
        return RemindersRepo.run_pandas_query(sql)
