# Target: tools for the app (db, wEvent, logger)
# Version: 0.1
# Date: 2017/01/18
# Author: Guillain (guillain@gmail.com)

from flask import Flask
from flask import flash
from HTMLParser import HTMLParser
import MySQLdb

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTING')

# Log function (push in flash + log)
def logger(fct,msg):
  flash(msg)
  print(str(fct+": "+msg))
  return

# Event function: logger + SQL records
def wEvent(module, user, msg):
    logger(module,msg)
    return exeReq("INSERT INTO events (module, user, msg) VALUES ('"+module+"', '"+user+"', '"+msg+"');")

# MySQL connection
def connection():
    conn = MySQLdb.connect(
        host = app.config['MYSQL_HOST'],
        user = app.config['MYSQL_USER'],
        passwd = app.config['MYSQL_PASSWORD'],
        db = app.config['MYSQL_DB']
    )
    c = conn.cursor()
    return c, conn

# SQL execution
def exeReq(req):
    error = None

    try:
        c, conn = connection()
    except Exception as e:
        logger('DB connection issue')
        return e

    try:
        c.execute(req)
        conn.commit()
    except Exception as e:
        logger('DB req execution issue')
        return e

    try:
        d = c.fetchall()
        c.close()
        return d
    except Exception as e:
        logger('DB fetch data issue')
        return e

# HTML Striper
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

