from flask import Flask , render_template, request ,redirect , url_for ,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import routes
app = Flask(__name__)
mysql = MySQL(app)
app.config.from_pyfile('config.py')
