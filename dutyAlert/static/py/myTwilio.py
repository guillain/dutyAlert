# Target: Twilio specific integration
# Version: 0.1
# Date: 2017/01/15
# Author: Guillain SANCHEZ
# Author: Guillain (guillain@gmail.com)

# Add mobile phone number to be checked
# twilio.com/user/account/phone-numbers/verified

from flask import Flask
from flask import render_template
from twilio.rest import TwilioRestClient
#from flask_mysqldb import MySQL
from tools import logger, exeReq, wEvent
 
from flask import Blueprint
twilio_api = Blueprint('twilio_api', __name__)

# Conf app
api = Flask(__name__)
api.config.from_object(__name__)
api.config.from_envvar('FLASK_SETTING')

# SMS functions  
def sms(to, msg):
  if not to:
    wEvent('sendSms','app',str("No phone number provided"))
    return ''
  if not msg:
    wEvent('sendSms','app',str("No message provided"))
    return ''

  client = TwilioRestClient(api.config['TWILIO_ACCOUNT_SID'], api.config['TWILIO_AUTH_TOKEN'])
  client.messages.create(
    to = to,
    from_ = api.config['TWILIO_FROM'],
    body = msg,
  )
  return client

# Call functions
def call(to, url):
  if not to:
    wEvent('sendCall','app',str("No phone number provided"))
    return ''
  if not url:
    wEvent('sendCall','app',str("No url provided"))
    return ''

  client = TwilioRestClient(api.config['TWILIO_ACCOUNT_SID'], api.config['TWILIO_AUTH_TOKEN'])
  client.calls.create(
    to = to,
    from_ = api.config['TWILIO_FROM'],
    url = url,
    #media_url="https://climacons.herokuapp.com/clear.png",
  )

  return client

# Call and tts message functions
def calltts(to, msg):
  if not to:
    wEvent('sendCall','app',str("No phone number provided"))
    return ''
  if not msg:
    wEvent('sendCall','app',str("No message provided"))
    return ''

  client = TwilioRestClient(api.config['TWILIO_ACCOUNT_SID'], api.config['TWILIO_AUTH_TOKEN'])
  client.calls.create(
    to = to,
    from_ = api.config['TWILIO_FROM'],
    url = msg,
    #media_url="https://climacons.herokuapp.com/clear.png",
  )

  return client

def shutup():
  return render_template('spark.html')

  for call in client.calls.iter(status=Call.QUEUED):
    call.hangup()

  for call in client.calls.iter(status=Call.RINGING):
    call.hangup()

  for call in client.calls.iter(status=Call.IN_PROGRESS):
    call.hangup()

  return 'OK'
