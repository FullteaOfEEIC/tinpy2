CREATE SCHEMA IF NOT EXISTS tinpy2;
USE tinpy2;

CREATE TABLE IF NOT EXISTS user(
  id CHAR(24) PRIMARY KEY,
  date DATETIME,
  name VARCHAR(256),
  age INT,
  gender INT,
  distance_mi BIGINT,
  bio VARCHAR(1600),
  jobs VARCHAR(100),
  schools VARCHAR(100),
  matched BOOLEAN
);

CREATE TABLE IF NOT EXISTS matches(
  match_id VARCHAR(128) PRIMARY KEY,
  created_date DATETIME,
  user_id CHAR(24),
  dead BOOLEAN,
  closed BOOLEAN
);

CREATE TABLE IF NOT EXISTS messages(
  id VARCHAR(128) PRIMARY KEY,
  match_id VARCHAR(128),
  created_date DATETIME,
  to_ CHAR(24),
  from_ CHAR(24),
  message VARCHAR(2400)
);
