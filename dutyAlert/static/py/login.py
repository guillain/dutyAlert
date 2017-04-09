#!/bin/python
# Target: login feature for duty alert system
# Version: 0.1
# Date: 2017/01/18
# Author: Guillain (guillain@gmail.com)
# Copyright 2017 GPL - Guillain

from flask import Flask, session
from tools import logger, exeReq, wEvent

# Conf app
api = Flask(__name__)
api.config.from_object(__name__)
api.config.from_envvar('FLASK_SETTING')

def userlogin(login,password):

    if not login or not password:
        logger('login','Thanks to provide login and password')
        return 'ko'

    try:
        sql  = "SELECT u.email, u.landline, u.mobile, u.accesstoken, m.roomid, m.teamid "
        sql += "FROM users u, mapping m "
        sql += "WHERE u.login = '" + login + "' AND pw_hash=PASSWORD('" + password + "') AND u.uid = m.uid "
        data = exeReq(sql)
    except Exception as e:
        logger('login','DB connection/request error!')
        return 'ko'

    if data is None:
        logger('login','Wrong email or password!')
        return 'ko'
    else:
        session['logged_in'] = True
        session['login'] = login
        session['email'] = data[0][0]
        session['mobile'] = data[0][2]
        session['accesstoken'] = ""
        session['roomid'] = data[0][4]
        session['teamid'] = data[0][5]

        if data[0][3]: # if accesstoken set so finalize the login
            session['accesstoken'] = "Bearer "+data[0][3]
            logger('login','You were logged (login:'+login+',email:'+session['email']+').')
            return 'ok'
        else: # no accesstoken so Cisco registration request
            logger('login','You were logged but without access token, redirect on AT request page ongoing (login:'+login+',email:'+session['email']+').')
            return 'accesstoken'

    return 'ko'
