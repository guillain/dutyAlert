# Database
## The structure is ready for Analytics!
At this time only one database is used but the target is to have two.
It's why you'll find in the [tools python file](dutyAlert/static/py/tools.py) specific functions for:
* database access (MySQL for now)
* logger functions named:
* * wEvents
* * logger
The idea is to be ready to move the applications events and user data into NoSQL database.
So the system is ready for just the databse and connector must be added.

## Oriented object database
Each object as user, group and id are stored and them specific tables.
One another table make the mapping between each object and it's the _mapping_ table as define below:
```bash
  mid integer primary key auto_increment,
  uid integer,
  gid integer,
  roomid integer,
  teamid integer,
  peopleid integer,
  msgid integer,
  admin boolean,
  moder boolean,
  level integer
```
This allow to have mapping for 
* user to group, room, team, people, msg with different level access
But becareeful, only one user can be registered and have one single netry for teamid and roomid.

## Databse structure
The database structure is define as bellow and following the table's structure:
* users: user's profil
```bash
  uid integer primary key auto_increment,
  login varchar(32) not null,
  email varchar(64) not null,
  landline varchar(16) not null,
  mobile varchar(16) not null,
  pw_hash text not null,
  accesstoken text not null,
  creationdate date not null,
  UNIQUE KEY (login),
  UNIQUE KEY (email)
```
* groups: group for the users
```bash
  gid integer primary key auto_increment,
  name varchar(32) not null,
  description text not null,
  creationdate date,
  UNIQUE KEY (name)
```
* sid: to record locally specific id of Cisco Spark room, team, people and message
```bash
  sid integer primary key auto_increment,
  id varchar(92) not null,
  type varchar(32) not null,
  description text not null,
  creationdate date,
  UNIQUE KEY (id)
```

