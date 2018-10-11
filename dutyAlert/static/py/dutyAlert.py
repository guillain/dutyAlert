#!/bin/python
# Target: Duty alert
# Version: 0.1
# Date: 2017/01/18
# Author: Guillain (guillain@gmail.com)
# Copyright 2017 GPL - Guillain
#
# dutyAlert main script that manage the scenario.
# For that features are picked up from
# libraries and api.

from flask import Flask, request, render_template, redirect
from flask import url_for, jsonify, session
from tools import logger, exeReq, wEvent

import re, os, sys, urllib, base64
from pyCiscoSpark import get_room, post_room, post_message, post_roommembership
from myTwilio import sms, call
from tools import logger, exeReq, wEvent
from mail import sendMail

from flask import Blueprint
dutyAlert_api = Blueprint('dutyAlert_api', __name__)

# Conf app
api = Flask(__name__)
api.config.from_object(__name__)
api.config.from_envvar('FLASK_SETTING')


# Duty Alert mgt --------------------------------------------------------------------------
def dutyAlert():
  wEvent('dutyAlert','START',str('Start Alert duty process'))
  roomname = api.config['APP_SPACE_NAME']
  status = 'OK'

  # Create Spark room instead if DUTY ALERT ROOM ID is recorded in the user profil
  if session['roomid']:
    # Get Duty room
    try:
      room = get_room(session['accesstoken'],session['roomid'])
      wEvent('dutyAlert','getroom',str(session['roomid'] + " Duty room getting"))
    except Exception as e:
      wEvent('dutyAlert','getroom',str(session['roomid'] + " Issue during room getting"))
      return 'KO'
  else:
    # Duty room creation
    try:
      room = post_room(session['accesstoken'],roomname)
      wEvent('dutyAlert','setroom',str(room['id'] + " Duty room creation"))
    except Exception as e:
      wEvent('dutyAlert','setroom',str("Issue during room creation (name:"+roomname+")"))
      return 'KO'

  # Prepare message
  roomlink = re.split('ciscospark://us/ROOM/', str(base64.b64decode(room['id'])))
  roommsg  = api.config['APP_SPACE_MSG']
  roommsg += '* Space name: ' + roomname + '\n'
  roommsg += '* Space id: ' + room['id'] + '\n'
  roommsg += '* Space web url: ' + 'https://web.ciscospark.com/#/rooms/' + str(roomlink[1]) + '\n'
  roommsg += '* Space web url for login: ' + 'https://web.ciscospark.com/#/launch/rooms/' + str(roomlink[1]) '\n'
  roommsg += '* Space app url: ' + 'spark://rooms/' + str(roomlink[1]) +'\n'
  roommsg += '* Duty login: ' + session['login'] + '\n'
  roommsg += '* Duty mobile: ' + session['mobile'] + '\n'
  roommsg += '* Duty mail: ' + session['email']
  wEvent('dutyAlert','roommsg',room['id'] + ' ' + str(roommsg))

  # Add user room membership instead if DUTY TEAM ID is recorded in the user profil
  if session['teamid']:
    # Add team in the duty room
    try:
      membership = post_roommembership(session['accesstoken'],room['id'],session['teamid'],'true')
      wEvent('dutyAlert','team membership',str(room['id'] + " Duty team room membership " + session['teamid']))
    except Exception as e:
      status = 'KO'
      wEvent('dutyAlert','team membership',str(room['id'] + " Issue during team room membership " + session['teamid']))

  else:
    # Add user in the duty room
    try:
      membership = post_roommembership(session['accesstoken'],room['id'],session['email'],'true')
      wEvent('dutyAlert','user membership',str(room['id'] + " Duty room membership " + session['email']))
    except Exception as e:
      status = 'KO'
      wEvent('dutyAlert','user membership',str(room['id'] + " Issue during room membership " + session['email']))

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
    resMail = sendMail(api.config['APP_MAIL_HOST'],api.config['APP_MAIL'],session['email'],roommsg)
    wEvent('dutyAlert','email',str(room['id'] + " Duty email processing"))
  except Exception as e:
    wEvent('dutyAlert','email',str(room['id'] + " Issue during email processing"))

  # End of Duty Alert auto treatment
  wEvent('dutyAlert','END',str(room['id'] + " Duty Alert created, status: " + status))
  return str("Duty call alert done, status "+status)

