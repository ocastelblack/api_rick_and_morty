-- schema.sql

DROP TABLE IF EXISTS user CASCADE;
DROP TABLE IF EXISTS task CASCADE;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    due_date DATE,
    status TEXT DEFAULT 'Pendiente',
    user_id INTEGER NOT NULL,
    character_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES user(id)
);
