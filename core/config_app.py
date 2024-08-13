import os

DEFAULT_USER = 'postgres'
DEFAULT_PWD = 'postgres'
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = '5432'

DEFAULT_DATABASE = os.environ.get('DEFAULT_DATABASE', 'sdb')

DEFAULT_DB_SCHEMA = os.environ.get('DEFAULT_DB_SCHEMA', 'public')

DEFAULT_DATABASE_URL = os.environ.get(
    'DEFAULT_DATABASE_URL',
    f'postgresql://{DEFAULT_USER}:{DEFAULT_PWD}@{DEFAULT_HOST}:{DEFAULT_PORT}/{DEFAULT_DATABASE}'
)

SQLALCHEMY_TRACK_MODIFICATIONS = int(os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', '0')) == 1
SQLALCHEMY_ECHO = int(os.environ.get('SQLALCHEMY_ECHO', '0')) == 1
FLASK_DEBUG = int(os.environ.get('FLASK_DEBUG', '0')) == 1

SECRET_KEY = os.environ.get('SECRET_KEY', '6cda463d-78a5-4796-a4d8-1746664743f7')