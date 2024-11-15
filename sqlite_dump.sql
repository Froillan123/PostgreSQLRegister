PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE registrations (
    id SERIAL PRIMARY KEY,
    idno TEXT UNIQUE NOT NULL,
    lastname TEXT NOT NULL,
    firstname TEXT NOT NULL,
    course TEXT NOT NULL,
    level TEXT NOT NULL,
    image TEXT NOT NULL
);
DELETE FROM sqlite_sequence;
COMMIT;
