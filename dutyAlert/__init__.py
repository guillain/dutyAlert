# Target: app init 
# Version: 0.1
# Date: 2017/01/04
# Author: Guillain (guillain@gmail.com)
# Copyright 2017 GPL - Guillain

from flask import Flask, request, render_template, redirect
from flask import url_for, jsonify, flash, session
from static.py.tools import logger, exeReq, wEvent
import re, os

# Conf and create app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTING')

# Import ServiceDeskBot features
from static.py.dutyAlert import dutyAlert_api
app.register_blueprint(dutyAlert_api)


# WEB mgt ----------------------------------------------------------------------------
@app.route('/')
def my_form():
  if 'login' in session:
    return render_template("dutyAlert.html")
  return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        if not login or not password:
            logger('login','Thanks to provide login and password')
            return render_template('login.html')

        try:
            data = exeReq("SELECT email,landline,mobile,accesstoken FROM user WHERE login='"+login+"' AND pw_hash=PASSWORD('"+password+"')")
        except Exception as e:
            logger('login','DB connection/request error!')
            return render_template('login.html')

        if data is None:
            logger('login','Wrong email or password!')
            return render_template('login.html')
        else:
            session['logged_in'] = True
            session['login'] = login
            session['email'] = data[0][0]
            session['mobile'] = data[0][2]
            session['accesstoken'] = ""
            if data[0][3]: # if accesstoken set so finalize the login
              session['accesstoken'] = "Bearer "+data[0][3]
              logger('login','You were logged (login:'+login+',email:'+session['email']+').')
              return render_template('dutyAlert.html')
            else: # no accesstoken so Cisco registration request
              logger('login','You were logged but without access token, redirect on AT request page ongoing (login:'+login+',email:'+session['email']+').')
              return render_template('sparkauth.html')
    elif request.args.get("code"):
      return render_template('sparkauth.html')
    else:
      return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  session.clear()
  logger('logout','You were logged out')
  return render_template('login.html')

# Auth --------------------------------------------------------------------------------
@app.route('/sparkauth', methods=['GET', 'POST'])
def sparkauth():
  if request.method == 'POST':
    print 'sparkauth: dutyAlert.html'
    return render_template('dutyAlert.html')
  elif request.args.get("code"):
    print 'sparkauth: sparkauth.html'
    return render_template('sparkauth.html')
  else:
    print 'sparkauth: login.html'
    return render_template('login.html')

# Access token ------------------------------------------------------------------------
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

