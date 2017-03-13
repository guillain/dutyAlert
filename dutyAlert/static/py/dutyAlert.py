#!/bin/python
# Target: Duty alert
# Version: 0.1
# Date: 2017/01/18
# Author: Guillain (guillain@gmail.com)
# Copyright 2017 GPL - Guillain

from flask import Flask, request, render_template, redirect
from flask import url_for, jsonify, session
from tools import logger, exeReq, wEvent

import re, os, sys, urllib
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
  roomname = 'Duty Alert Space'
  roommsg = 'New Duty Alert raised!'
  status = 'OK'

  # Duty room creation
  try:
    room = post_room(session['accesstoken'],roomname)
    wEvent('dutyAlert','room',str("Duty room creation (name:"+roomname+", mobile:"+session['mobile']+")"))
  except Exception as e:
    status = 'KO'
    wEvent('dutyAlert','room',str("Issue during room creation (name:"+roomname+")"))

  # Duty room membership
  try:
    membership = post_roommembership(session['accesstoken'],room['id'],session['email'],'true')
    wEvent('dutyAlert','room',str("Duty room membership (name:"+roomname+", member:"+session['email']+")"))
  except Exception as e:
    status = 'KO'
    wEvent('dutyAlert','room',str("Issue during room membership (email:"+session['email']+")"))

  # Duty room message post
  try:
    msg = post_message(session['accesstoken'],room['id'],roommsg)
    wEvent('dutyAlert','message',str("Duty room message post (name:"+roomname+", msg:"+roommsg+")"))
  except Exception as e:
    status = 'KO'
    wEvent('dutyAlert','room',str("Issue during post message (name:"+roomname+")"))

  # Duty sms processing
  try:
    sms(session['mobile'],str('DUTY ALERT: thanks to join Spark to consult alert.\nSpace name:'+roomname+',Space id:'+room['id']))
    wEvent('dutyAlert','sms',str("Duty sms processing (name:"+roomname+", room id:"+room['id']+", mobile:"+session['mobile']+")"))
  except Exception as e:
    wEvent('dutyAlert','sms',str("Issue during sms processing (name:"+roomname+")"))

  # Duty call processing
  try:
    call(session['mobile'],'http://hosting.tropo.com/48562/www/audio/7gramrocks.mp3')
    wEvent('dutyAlert','call',str("Duty call processing OK (name:"+roomname+", room id:"+room['id']+", mobile:"+session['mobile']+")"))
  except Exception as e:
    wEvent('dutyAlert','call',str("Issue during call processing (name:"+roomname+")"))

  # End of Duty Alert auto treatment
  wEvent('dutyAlert','app',str("Duty Alert created, status: "+status+" (room name:"+roomname+", room id:"+room['id']+", mobile:"+session['mobile']+")"))
  return str("Duty call alert done, status "+status)

