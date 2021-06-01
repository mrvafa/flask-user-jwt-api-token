import os
from pathlib import Path

basedir = Path(__file__).resolve().parent
sqlite_local_base = 'sqlite:///../'
database_name = 'db.sqlite3'


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'e9da0ef46c177336178515bb')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = sqlite_local_base + database_name


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = sqlite_local_base + database_name + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
