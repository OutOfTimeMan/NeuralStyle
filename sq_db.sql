CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
email text NOT NULL,
psw text NOT NULL,
image BLOB DEFAULT NULL,
styleID integer DEFAULT 1,
time integer DEFAULT NULL
);