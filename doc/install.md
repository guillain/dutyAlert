# Install

## Clone localy
```bash
git clone https://github.com/guillain/dutyAlert.git
```

## Configure and set apache configuration
Default apache configuration are provided for http and https web access.
This can work in parallel of manual execution for dev in parallel of prod (can be usefulll... ;).


* For unsecure http (80)
```bash
cp conf/dutyAlert_apache.conf.default conf/dutyAlert_apache.conf
vi conf/dutyAlert_apache.conf (ServerName must be replaced)
ln -s /var/www/dutyAlert/conf/dutyAlert_apache.conf /etc/apache2/conf-enabled/dutyAlert_apache.conf
```

* For secure http (443)
Rember to have a valid chain of certificate and specificly signed by public authority to be used with cloud services (Cisco Spark, Twilio...).
```bash
cp conf/dutyAlert_apache-secure.conf.default conf/dutyAlert_apache_secure.conf
vi conf/dutyAlert_apache-secure.conf (ServerName must be replaced, certificate must be adapted)
ln -s /var/www/dutyAlert/conf/dutyAlert_apache-secure.conf /etc/apache2/conf-enabled/dutyAlert_apache-secure.conf
```

## Configure the database
Edit the file conf/mysql_data.sql to adapt it to your set, user, group and spark env.
And import the database structure following by the data insertion.
```bash
mysqladmin create dutyAlert -uroot -ppassword
mysql dutyAlert -uroot -ppassword < conf/mysql.sql
mysql dutyAlert -uroot -ppassword < conf/mysql_data.sql (add users can be useful...)
```

## Configure the dutyAlert application
Complete the default configuration file according to your environment.

Remember to have or create
* [Cisco Spark](http://developper.ciscospark.com) client ID and secret
* [Twilio](http://www.twilio.com) account SID and token
```bash
cp conf/settings.cfg.default conf/settings.cfg
vi conf/settings.cfg
```

## Test
* Put your url in the web browser
* Login with the user add in the conf/mysql_data.sql file
* If Cisco Spark token not already in the db, follow the process to get it and click on the shortcut below the login
* Click on the panel
* It's done :)
