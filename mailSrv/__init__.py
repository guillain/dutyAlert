# Target: mail server init 
# Version: 0.1
# Date: 2017/01/04
# Author: Guillain (guillain@gmail.com)
# Copyright 2017 GPL - Guillain

from mail import popSrvMail

MAIL_HOST = 'pop.gmail.com'
MAIL_USER = 'dutyAlertApp'
MAIL_PASS = 'C&1CptDutyAlert!'

(subject,content) = popSrvMail(MAIL_HOST,MAIL_USER,MAIL_PASS)
# ToDo: send REST request to the web server
print "subject: " + subject
print "content: " + content

# End of App --------------------------------------------------------------------------
#if __name__ == '__main__':
#    sess.init_app(app)
#    app.debug = app.config['DEBUG']
#    app.run()

