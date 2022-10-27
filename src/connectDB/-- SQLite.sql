-- SQLite
CREATE TABLE IF NOT EXISTS "Student" (
    "ID" INTEGER PRIMARY KEY ,
    "Name" VARCHAR(255)  ,
    "Class" VARCHAR(255) ,
    "Birthday" VARCHAR(255)  ,
    "Sex" VARCHAR(255)
);

DROP TABLE IF EXISTS "Student";