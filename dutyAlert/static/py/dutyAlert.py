#!/bin/python
# Target: Duty alert
# Version: 0.1
# Date: 2017/01/18
# Author: Guillain (guillain@gmail.com)
# Copyright 2017 GPL - Guillain

from flask import Flask, request, render_template, redirect
from flask import url_for, jsonify, session
from tools import logger, exeReq, wEvent

import re, os, sys, urllib, base64, smtplib
from email.mime.text import MIMEText
from pyCiscoSpark import post_room, post_message, post_roommembership
from myTwilio import sms, call
from tools import logger, exeReq, wEvent

from flask import Blueprint
dutyAlert_api = Blueprint('dutyAlert_api', __name__)

# Conf app
api = Flask(__name__)
api.config.from_object(__name__)
api.config.from_envvar('FLASK_SETTING')


# Duty Alert mgt --------------------------------------------------------------------------
@dutyAlert_api.route('/dutyAlert', methods=['POST'])
def dutyAlert():
  wEvent('dutyAlert','START',str('Start Alert duty process'))
  roomname = api.config['APP_SPACE_NAME']
  status = 'OK'

  # Duty room creation
  try:
    room = post_room(session['accesstoken'],roomname)
    wEvent('dutyAlert','room',str(room['id'] + " Duty room creation"))
  except Exception as e:
    wEvent('dutyAlert','room',str("Issue during room creation (name:"+roomname+")"))
    return 'KO'

  # Prepare message
  roomlink = re.split('ciscospark://us/ROOM/', str(base64.b64decode(room['id'])))

  roommsg = api.config['APP_SPACE_MSG']
  roommsg += '* Space name: ' + roomname + '\n'
  roommsg += '* Space id: ' + room['id'] + '\n'
  roommsg += '* Space web url: ' + 'https://web.ciscospark.com/rooms/' + str(roomlink[1]) + '/chat' + '\n'
  roommsg += '* Space app url: ' + 'spark://rooms/' + str(roomlink[1]) +'\n'
  roommsg += '* Duty login: ' + session['login'] + '\n'
  roommsg += '* Duty mobile: ' + session['mobile'] + '\n'
  roommsg += '* Duty mail: ' + session['email']
  wEvent('dutyAlert','roommsg',room['id'] + str(roommsg))

  # Duty room membership
  try:
    membership = post_roommembership(session['accesstoken'],room['id'],session['email'],'true')
    wEvent('dutyAlert','membership',str(room['id'] + " Duty room membership" + room['id']))
  except Exception as e:
    status = 'KO'
    wEvent('dutyAlert','membership',str(room['id'] + " Issue during room membership"))

  # Duty room message post
  try:
    msg = post_message(session['accesstoken'],room['id'],roommsg)
    wEvent('dutyAlert','message',str(room['id'] + " Duty room message post"))
  except Exception as e:
    status = 'KO'
    wEvent('dutyAlert','message',str(room['id'] + " Issue during post message"))

  # Duty sms processing
  try:
    sms(session['mobile'],roommsg)
    wEvent('dutyAlert','sms',str(room['id'] + " Duty sms processing"))
  except Exception as e:
    wEvent('dutyAlert','sms',str(room['id'] + " Issue during sms processing"))

  # Duty call processing
  try:
    call(session['mobile'],'http://www.tropo.com/docs/troporocks.mp3')
    wEvent('dutyAlert','call',str(room['id'] + " Duty call processing"))
  except Exception as e:
    wEvent('dutyAlert','call',str(room['id'] + " Issue during call processing"))

  # Duty send email
  try:
    msg = MIMEText(roommsg)
    msg['Subject'] = api.config['APP_SPACE_MSG']
    msg['From'] = api.config['APP_MAIL']
    msg['To'] = session['email']
    s = smtplib.SMTP('localhost')
    s.sendmail(api.config['APP_MAIL'], session['email'], msg.as_string())
    s.quit()
    wEvent('dutyAlert','email',str(room['id'] + " Duty email processing"))
  except Exception as e:
    wEvent('dutyAlert','email',str(room['id'] + " Issue during email processing"))

  # End of Duty Alert auto treatment
  wEvent('dutyAlert','END',str(room['id'] + " Duty Alert created, status: " + status))
  return str("Duty call alert done, status "+status)

