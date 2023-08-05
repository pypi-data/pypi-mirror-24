CREATE DATABASE kuorra_login;

USE kuorra_login;

CREATE TABLE users(
    username varchar(20) NOT NULL PRIMARY KEY,
    password varchar(32) NOT NULL,
    privilege integer NOT NULL DEFAULT 0
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE sessions(
    session_id char(128) UNIQUE NOT NULL,
    atime timestamp NOT NULL default current_timestamp,
    data text
);


INSERT INTO users(username, password, privilege) VALUES ('admin',MD5('admin'), 0);
INSERT INTO users(username, password, privilege) VALUES ('guess',MD5('guess'), 1);


SELECT * FROM users;
SELECT * FROM sessions;