/*
 @ Target: MySQL init data
 @ Version: 0.1
 @ Date: 2017/02/04
 @ Author: Guillain (guillain@gmail.com)
 @ Copyright 2017 GPL - Guillain
*/

INSERT INTO users (uid, login, email, landline, mobile, pw_hash, accesstoken) VALUES
  ('1', 'admin','admin@mail.com','+33987654321','+33654321012',PASSWORD('admin'),''),
  ('2', 'user' ,'user@mail.com','+33987654321','+33654321012',PASSWORD('user'),''),
  ('3', 'guest','guest@mail.com','+33987654321','+33654321012',PASSWORD('guest'),'');

INSERT INTO groups (gid, name, description, creationdate) VALUES
  ('1', 'admin','Admin group',NOW()),
  ('2', 'user' ,'User group',NOW()),
  ('3', 'guest','Guest group',NOW());

INSERT INTO ids (sid,id,type,description) VALUES
  ('1', 'abcdefghijklmnopqrstuvwxyz0123456789abcdefghijklmnopqrstuvwxyz0123456789abcdefg', 'roomid','roomid example'),
  ('2', 'abcdefghijklmnopqrstuvwxyz0123456789abcdefghijklmnopqrstuvwxyz0123456789abcdefg', 'teamid','teamid example');

INSERT INTO mapping (uid, gid, admin, moder, roomid, teamid) VALUES
  ('1','1','1','1','',''),
  ('2','2','1','0','1','2'),
  ('3','3','0','0','','');


