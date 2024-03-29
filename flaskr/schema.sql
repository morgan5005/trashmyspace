DROP TABLE IF EXISTS event_post;
DROP TABLE IF EXISTS event_announcement;
DROP TABLE IF EXISTS trashoverflow;

CREATE TABLE event_post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT,
  author_name TEXT NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  event_date TEXT NOT NULL
);

CREATE TABLE event_announcement (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  author_name TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  event_date NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE trashoverflow (
    id INTEGER PRIMARY KEY AUDOINCREMENT,
    location DOUBLE NOT NULL,
    trashcan_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
