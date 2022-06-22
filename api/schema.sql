create table if not exists Users (
    id integer primary key autoincrement,
    username text not null unique,
    passwordHash blob not null,
    firstname text,
    lastname text,
    email text unique,
    is_authenticated blob,
    is_active BLOB,
    is_anonymous blob
);

