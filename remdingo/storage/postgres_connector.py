from sqlalchemy import create_engine, text

from remdingo.config.config import Config


class DbConnector:
    def __init__(self):
        pass

    @staticmethod
    def get_remdingo_engine():
        print("*** create engine ****")
        return create_engine(Config.PSYCOPG_DATABASE_URI, pool_size=20, max_overflow=0, pool_recycle=2000)

    @staticmethod
    def execute_select(engine, query, params=None):
        connection = engine.connect()

        try:
            if params:
                result = connection.execute(text(query), params)
            else:
                result = connection.execute(text(query))
            return result
        except Exception as exception:
            raise exception

    @staticmethod
    def execute_query(engine, query, params=None):
        connection = engine.connect()
        trans = connection.begin()
        try:
            if params:
                connection.execute(text(query), params)
            else:
                connection.execute(text(query))
            trans.commit()
        except Exception as exception:
            raise exception

    @staticmethod
    def get_connection(engine):
        return engine.connect()
