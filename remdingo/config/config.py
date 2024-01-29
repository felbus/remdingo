import os
from datetime import timedelta


# noinspection SpellCheckingInspection
class Config:
    environment = os.environ.get("REMDINGO_ENVIRONMENT")
    docker = os.environ.get("REMDINGO_DOCKER")

    if environment == docker == "1":
        DB_PORT = '5432'
        DB_HOST = "postgres"
    else:
        DB_PORT = '5435'
        DB_HOST = "127.0.0.1"

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    SECRET_KEY = "aaoorewqppgmdnbbxskr"
    SESSION_COOKIE_NAME = "cookie_fash"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

    RECAPTCHA_PUBLIC_KEY = "iubhiukfgjbkhfvgkdfm"
    RECAPTCHA_PARAMETERS = {"size": "100%"}

    DB_USERNAME = "postgres"
    DB_PASSWORD = "remdingo5435434"

    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_TIMEOUT = 300
    SQLALCHEMY_DB_SCHEMA = "public"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_NAME = "remdingodb"
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{SQLALCHEMY_DATABASE_NAME}'
    PSYCOPG_DATABASE_URI = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{SQLALCHEMY_DATABASE_NAME}'

    # Flask-Login
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
