CREATE TABLE SubsDB ( subid TEXT PRIMARY KEY, userid TEXT, event TEXT, target_url TEXT );
CREATE TABLE UserDB ( userid TEXT PRIMARY KEY, username TEXT, password TEXT , permissions integer);
CREATE INDEX EventIdx ON SubsDB ( event );
CREATE TABLE TokenDB ( token TEXT PRIMARY KEY, userid TEXT , device_name TEXT, time_create integer);
CREATE TABLE DevcodeDB ( devcode TEXT PRIMARY KEY , claimed char(1), userid TEXT, time_create integer);
INSERT INTO UserDB VALUES ( '001', 'mossy', 'mossymossy', 7 );
INSERT INTO UserDB VALUES ( '002', 'oona', 'oonaoona', 3 );
INSERT INTO UserDB VALUES ( '003', 'baba', 'babababa', 1 );
