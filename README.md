# dutyAlert
* Cisco Spark
* Twilio
...to raise alert and wake the duty guy

## What is it?
It's a form form with local authentication who:
* store in session the profil coming from the local
* create a Cisco Spark room
* associate its member to the Cisco Spark room
* post the alert message in the Cisco Spark room
* send SMS via Twilio
* perform a call via Twilio
All of that with Event manage

## PreRequisites
Configuration is provided for Apache and WSGI server.
But you can also get only the python with another web server, container...
* Apache2
* MySQL
* python (2.7)
* * Flask
* * MySQLdb
* * twilio

## Install

### Clone localy
> git clone https://github.com/guillain/dutyAlert.git

### Configure and set apache configuration
* For unsecure http (80)

> cp conf/dutyAlert_apache.conf.default conf/dutyAlert_apache.conf
> vi conf/dutyAlert_apache.conf (ServerName must be replaced)
> ln -s /var/www/dutyAlert/conf/dutyAlert_apache.conf /etc/apache2/conf-enabled/dutyAlert_apache.conf

* For secure http (443)

> cp conf/dutyAlert_apache-secure.conf.default conf/dutyAlert_apache_secure.conf
> vi conf/dutyAlert_apache-secure.conf (ServerName must be replaced, certificate must be adapted)
> ln -s /var/www/dutyAlert/conf/dutyAlert_apache-secure.conf /etc/apache2/conf-enabled/dutyAlert_apache-secure.conf

### Configure the database
> mysqladmin create dutyAlert -utoto -p
> mysql dutyAlert -utoto -p < conf/mysql.sql
> mysql dutyAlert -utoto -p < conf/mysql_data.sql (add users can be useful...)

### Configure the dutyAlert application
Remember to have or create
* [Cisco Spark](http://developper.ciscospark.com) client ID and secret
* [Twilio](http://www.twilio.com) account SID and token

> cp conf/settings.cfg.default conf/settings.cfg
> vi conf/settings.cfg

### Run the application
Two configuration availables

1/ For the dev, node is used

> vi run (adapt at least the path)
> ./run manual

2/ For the prod, pm2 is used (install also this dependency)

> ./app [start|stop|restart|staus]

### Test
* Put your url in the web browser
* Login with the user add in the conf/mysql_data.sql file
* If Cisco Spark token not already in the db, follow the process to get it and click on the shortcut below the login
* Click on the panel
* It's done :)


### Troubleshooting
Start with the dev run mode and follow the traces in the screen.
This should be the good point to start... As for all troubleshooting... logs first ;)
If no specific issue appear you can follow the action plan hereafter.

Token access = TA

* No Spark space created: 
* * Are you sure about your Cisco Spark TA?
* * If you use this Cisco Spark TA with postman it works?
* No SMS: Twilio
* * As for Cisco Spark, check your Twilio TA
* * Be sure that:
* * * The phone number is authorized
* * * The number can send SMS
* No Call: Twilio
* * Same as for SMS (instead the SMS feature of course)


Have fun
