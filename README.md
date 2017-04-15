# dutyAlert
* Cisco Spark
* Twilio
...to raise alert and wake the duty guy
...but more than that...

## What is it?
It's a system to raise alert coming from:
* Web event
* * for that web form is provided for the demo
* Mail
* * for that mailbox is pooling (option can be added to filter subject for the moment new emails are catched)
* * imap and pop features are provided

It will inform:
* In the Cisco Spark room:
* * Only the duty guy and admin if no team id recorded in the user profil
* * the team and associated member if team id is provided in the session
* On phone:
* * sms and call for the duty guy only
* By mail:
* * to send back report to original montiroign system

The alert is provided on:
* Cisco Spark room
* * if roomid is provided in the user profil, the room is updated with the new alert message + details
* * if not, new room is created and alert message + details are posted into
* * (these two behaviors are more oriented to have the capability to follow one specific room vs. create new room than allow one specific room each time and record the first room id done during the creation for permananet record (but this can be add in update sql request of course))
* SMS
* * The same message as posted in the Cisco Spark room to provide info on the mobile
* Call
* * To wake up the guy
* * The idea is to be sure that the guy is ready

## Scenario
* Get Mail on mailbox (filter on subekct and/or content, not finalized)
* Create/update Cisco Spark space
* Send SMS to duty guy with formatted message
* Call the duty with message to voice 
* Send back email as report

## Features
* Web interface to manage users and group
* Can create a new Cisco Spark space or used one associated to the user or team
* Can associate user (group management included) or team
* Escalation process is launched (add membership or team) of 'escalation' keywork is enter

## Without mail server
Thanks to use the version 1.0.x

## The database explanation
[doc/database.md](doc/database.md)

## The improvement ideas
[doc/todo.md](doc/todo.md)

## PreRequisites
[doc/prerequisites.md](doc/prerequisites.md)

## Install
[doc/install.md](doc/install.md)

## Troubleshooting
[doc/troubleshooting.md](doc/troubleshooting.md)

## Report bug
[issues](issues)



Have fun ;)
