# Troubleshooting
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

