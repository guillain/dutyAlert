#!/bin/python
# Target: Mail sender for duty Alert
# Version: 0.1
# Date: 2017/01/18
# Author: Guillain (guillain@gmail.com)
# Copyright 2017 GPL - Guillain

from flask import Flask
import re, os, sys, smtplib, poplib, imaplib
from email.mime.text import MIMEText
from email.parser import Parser

# Send mail -------------------------------------------------------------------------------
def sendMail(host,fromu,to,text):

  try:
    # Create a text/plain message
    msg = MIMEText(text)

    msg['Subject'] = 'The contents of %s' 
    msg['From'] = fromu
    msg['To'] = to

    # Send the message via our own SMTP server, but don't include the # envelope header.
    s = smtplib.SMTP(host)
    s.sendmail(fromu, to, msg.as_string())
    s.quit()

    return 'ok'
  except Exception as e:
    return e

# IMAP server mail
def imapSrvMail(host,user,password,to,subject):

  # IMAP connection & find unread emails
  conn = imaplib.IMAP4_SSL(host)
  try:
    (retcode, capabilities) = conn.login(user, password)
  except:
    print sys.exc_info()[1]
    sys.exit(1)
  conn.select(readonly=1) # Select inbox or default namespace

  (retcode, messages) = conn.search(None, '(UNSEEN)')
  if retcode == 'OK':
    for num in messages[0].split(' '):
      print 'Processing :', message
      typ, data = conn.fetch(num,'(RFC822)')
      msg = email.message_from_string(data[0][1])
      typ, data = conn.store(num,'-FLAGS','\\Seen')
      if ret == 'OK':
        return (msg,data)
  conn.close()

  return 'ok'

# POP server mail
def popSrvMail(host,user,password):
  import poplib
  from email import parser
  mails = {}

  pop_conn = poplib.POP3_SSL(host)
  pop_conn.user(user)
  pop_conn.pass_(password)

  #Get messages from server:
  messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]

  # Concat message pieces:
  messages = ["\n".join(mssg[1]) for mssg in messages]

  #Parse message intom an email object:
  messages = [parser.Parser().parsestr(mssg) for mssg in messages]
  for message in messages:
    print ">>> Subject: " + str(message['subject'])

    # Parse mail body and return text message
    for part in message.walk():
      if part.get_content_type():
        charset = part.get_content_charset()
        if charset:
          content = part.get_payload(decode=True)
          content = content.decode(charset).encode('utf-8')
          print ">>> Content: " + str(content)
          return (message['subject'],content)
  pop_conn.quit()

  # No new mail
  return '0'
