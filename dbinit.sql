# NOTE: the schema is created automatically by peewee
CREATE TABLE IF NOT EXISTS "subscription" ("id" INTEGER NOT NULL PRIMARY KEY, "user_id" INTEGER NOT NULL, "event" VARCHAR(255) NOT NULL, "target_url" VARCHAR(255) NOT NULL, FOREIGN KEY ("user_id") REFERENCES "user" ("id"));
CREATE INDEX "subscription_user_id" ON "subscription" ("user_id");
CREATE INDEX "subscription_event" ON "subscription" ("event");
CREATE TABLE IF NOT EXISTS "user" ("id" INTEGER NOT NULL PRIMARY KEY, "username" VARCHAR(255) NOT NULL, "password" VARCHAR(255) NOT NULL, "permissions" INTEGER NOT NULL);
CREATE UNIQUE INDEX "user_username" ON "user" ("username");
CREATE TABLE IF NOT EXISTS "token" ("id" INTEGER NOT NULL PRIMARY KEY, "token" VARCHAR(255) NOT NULL, "user_id" INTEGER NOT NULL, "device_name" VARCHAR(255) NOT NULL, "time_create" INTEGER NOT NULL, FOREIGN KEY ("user_id") REFERENCES "user" ("id"));
CREATE UNIQUE INDEX "token_token" ON "token" ("token");
CREATE INDEX "token_user_id" ON "token" ("user_id");
CREATE TABLE IF NOT EXISTS "devcode" ("id" INTEGER NOT NULL PRIMARY KEY, "devcode" VARCHAR(255) NOT NULL, "time_create" INTEGER NOT NULL);
CREATE UNIQUE INDEX "devcode_devcode" ON "devcode" ("devcode");
