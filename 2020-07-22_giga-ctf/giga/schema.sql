DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS downl;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  ip TEXT NOT NULL,
  question TEXT NOT NULL, 
  answer TEXT NOT NULL
);

CREATE TABLE downl (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  file_path TEXT NOT NULL,
  user_id INTEGER NOT NULL
);


INSERT INTO user VALUES(1,"superadmin@alphamail.ctf","hunter2","aaaa0.0.1", "What are your favourite 128 random chars", "BGQlcX29KnXyVV7ahDe2U7oneceXYWBnhiaVJH0JujhnIB2hqpZL3lGUhawVgSQmsKWAc5AL42a8FWxq2fgT8T5sZ09MJy6bGX8X9zPqoePjeswmXfqSM6nAYKRt2Bpw");
INSERT INTO downl VALUES (1, "Flag.txt", "flag.txt", 1);
INSERT INTO downl VALUES (2, "I hate git", 'git.eml', 1);
INSERT INTO downl VALUES (3, "Memno-Books", 'mmeno.eml', 1);


