# Target: app init 
# Version: 0.1
# Date: 2017/01/04
# Author: Guillain (guillain@gmail.com)
# Copyright 2017 GPL - Guillain

from flask import Flask, request, render_template, redirect
from flask import url_for, jsonify, flash, session
from multiprocessing import Pool
from static.py.dutyAlert import dutyAlert
from static.py.login import userlogin
from static.py.tools import logger, exeReq, wEvent
import re, os

# Conf and create app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTING')

# Import ServiceDeskBot features
from static.py.dutyAlert import dutyAlert_api
app.register_blueprint(dutyAlert_api)


# MAIL mgt ----------------------------------------------------------------------------
def mailSrv():
  (subject,content) = popSrvMail(api.config['MAIL_HOST'],api.config['MAIL_USER'],api.config['MAIL_PASS'])
  # ToDo: session setting
  # resDutyAlert = dutyAlert() 
  wEvent('dutyAlert','popSrvMail','Subject: ' + subject + ', content: ' + content)
  return 'ok'


# WEB mgt ----------------------------------------------------------------------------
@app.route('/')
def my_form():
  if 'login' in session:
    return render_template("dutyAlert.html")
  return render_template("login.html")

@app.route('/dutyAlert', methods=['POST'])
def webDutyAlert():
  return dutyAlert()

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Web POST login request
    if request.method == 'POST':
        resUser = userlogin(request.form['login'],request.form['password'])
        if   (resUser == 'ok'):
            return render_template('dutyAlert.html')
        elif (resUser == 'accesstoken'):
            return render_template('sparkauth.html')
        else:
            return render_template('login.html')

    # Spark auth back reply
    elif request.args.get("code"):
        return render_template('sparkauth.html')

    # Web GET login request
    elif request.method == 'GET':
        try:
            if session['accesstoken']:
                return render_template('dutyAlert.html')
        except Exception as e:
            return render_template('login.html')

    # Error
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  session.clear()
  logger('logout','You were logged out')
  return render_template('login.html')

# Spark auth --------------------------------------------------------------------------------
@app.route('/sparkauth', methods=['GET', 'POST'])
def sparkauth():
  if request.method == 'POST':
    return render_template('dutyAlert.html')
  elif request.args.get("code"):
    return render_template('sparkauth.html')
  else:
    return render_template('login.html')

# Spark save Access token ------------------------------------------------------------------------
@app.route('/saveAT', methods=['POST'])
def saveAT():
    error = None
    try:
        data = exeReq("UPDATE user SET accesstoken = '"+request.form['token']+"' WHERE login='"+session['login']+"'")
    except Exception as e:
        logger('saveAT','DB connection/request error!')
        return render_template('login.html', error = error)

    session['accesstoken'] = request.form['token']
    logger('saveAT','Your access token was recorded properly')
    return redirect(url_for('logout'))

# Spark reset Access token ------------------------------------------------------------------------
@app.route('/resetAT', methods=['POST'])
def resetAT():
    error = None
    try:
        data = exeReq("UPDATE user SET accesstoken = '' WHERE login='"+session['login']+"'")
    except Exception as e:
        logger('saveAT','DB connection/request error!')
        return render_template('login.html', error = error)

    session['accesstoken'] = ''
    logger('saveAT','Your access token was resetted properly')
    return redirect(url_for('logout'))

# End of App --------------------------------------------------------------------------
if __name__ == '__main__':
    sess.init_app(app)
    app.debug = True
    app.run()

    p = Pool(app.config['MAIL_POOL_FREQ'])
    p.map(mailSrv)

