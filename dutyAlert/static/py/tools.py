# Target: tools for the app (db, wEvent, logger)
# Version: 0.1
# Date: 2017/01/18
# Author: Guillain SANCHEZ
# Author: Guillain (guillain@gmail.com)

from flask import Flask
from flask import flash
import MySQLdb

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTING')

# FUNCTIONs ---------------------------
# Log function (push in flash + log)
def logger(fct,msg):
  flash(msg)
  print(str(fct+": "+msg))
  return

def connection():
    conn = MySQLdb.connect(
        host = app.config['MYSQL_HOST'],
        user = app.config['MYSQL_USER'],
        passwd = app.config['MYSQL_PASSWORD'],
        db = app.config['MYSQL_DB']
    )
    c = conn.cursor()
    return c, conn


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

def wEvent(module, user, msg):
    logger(module,msg)
    return exeReq("INSERT INTO events (module, user, msg) VALUES ('"+module+"', '"+user+"', '"+msg+"');")


