USE $DB_NAME;

CREATE TABLE users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(256) NOT NULL,
	password VARCHAR(256) NOT NULL,
	ip VARCHAR(45) NOT NULL,
	session VARCHAR(256) NOT NULL
);
CREATE TABLE messages (
	id INT AUTO_INCREMENT PRIMARY KEY,
	user VARCHAR(256),
	subject VARCHAR(100) NOT NULL,
	content TEXT NOT NULL,
	visibility VARCHAR(10) DEFAULT 'public'
);
CREATE TABLE secret_plans_zhsBYN3c (
	id INT AUTO_INCREMENT PRIMARY KEY,
	flag VARCHAR(128) NOT NULL
);

CREATE USER '$DB_USER1' IDENTIFIED BY '$DB_USER1_PASS';
CREATE USER '$DB_USER2' IDENTIFIED BY '$DB_USER2_PASS';

GRANT SELECT,INSERT,UPDATE ON ${MYSQL_DATABASE}.users TO ${DB_USER1};

GRANT SELECT ON ${MYSQL_DATABASE}.messages TO ${DB_USER2};
GRANT SELECT ON ${MYSQL_DATABASE}.secret_plans_zhsBYN3c TO ${DB_USER2};

INSERT INTO secret_plans_zhsBYN3c (flag) VALUES("Starkiller base manhole cover but made of adamantium"),("Actual encryption for our data,"),("h0h0h0{5omet1me5_N0_SQLi_1s_s7ill_SQLi}");

INSERT INTO messages (user,subject,content,visibility) VALUES
	("System Announcements", "Welcome to our ranks", "Please report for training tommorrow at 0800 in the hangar. You will be assigned a unit.", "public"),
	("Trooper 2V6o3GA", "You show great promise!", "I heard the General mention a secret mission, there's probably more info in his private messages", "self"),
	("General Tux", "Message from your leader", "Today is the end of the Republic. The end of a regime that acquiesces to clear text passwords. At this very moment in a system far from here, the New Republic leaks their user data to the galaxy while secretly selling the same data to rogue ad companies of the Resistance. This fierce machine which you have built, upon which we stand will bring an end to the C-Suite", "public"),
	("General Tux", "###TOP-SECRET###", "Please do not transmit via droid.<br>Some rebel scum tried to access the table containing our secret plans. It was a close one!<br>The plans for our secret projects have been relocated to table secret_plans_zhsBYN3c. They will stay there until the completion of our encryption program.", "private"),
	("Trooper Bob", "Please clean after yourselves", "The armors for trainees always stink! Please be considerate and use space febreze once you're done with them.", "public"),
	("Trooper 0ldG33zer", "hello google", "cold toes<br>how do you pronounce yoda<br>space hats<br>what is bantha milk?", "self");
