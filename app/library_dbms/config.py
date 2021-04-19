""" Flask configuration """
from os import environ , path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = environ.get('SECRET_KEY')
MYSQL_HOST='localhost'
MYSQL_USER='root'
MYSQL_PASSWORD = 'shiva#mysql'
MYSQL_DB='library_dbms'
