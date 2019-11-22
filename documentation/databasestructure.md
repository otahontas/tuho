# Database structure

## Database Model in UML
[]

## Create TABLE statements

```
        date_created DATETIME,
        date_modified DATETIME,
        name VARCHAR(144) NOT NULL,
        username VARCHAR(144) NOT NULL,
        password VARCHAR(144) NOT NULL,
        role_id INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(role_id) REFERENCES role (id)
);
CREATE TABLE chord (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        "key" VARCHAR(144) NOT NULL,
        name VARCHAR(144) NOT NULL,
        account_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(account_id) REFERENCES account (id)
);
CREATE TABLE song (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        name VARCHAR(144) NOT NULL,
        artist VARCHAR(144) NOT NULL,
        account_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(account_id) REFERENCES account (id)
);
CREATE TABLE chord_note (
        id INTEGER NOT NULL,
        chord_id INTEGER NOT NULL,
        note_id INTEGER NOT NULL,
        rank INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(chord_id) REFERENCES chord (id),
        FOREIGN KEY(note_id) REFERENCES note (id)
);
CREATE TABLE song_chord (
        id INTEGER NOT NULL,
        song_id INTEGER NOT NULL,
        note_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(song_id) REFERENCES song (id),
        FOREIGN KEY(note_id) REFERENCES chord (id)
);
CREATE TABLE user_favourite_song (
        id INTEGER NOT NULL,
        song_id INTEGER NOT NULL,
        account_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(song_id) REFERENCES song (id),
        FOREIGN KEY(account_id) REFERENCES account (id)
);
```
