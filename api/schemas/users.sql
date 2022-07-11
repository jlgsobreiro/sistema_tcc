create table if not exists Users (
    _id integer primary key autoincrement,
    username text not null unique,
    passwordHash blob not null,
    firstname text not null ,
    lastname text not null ,
    email text unique not null ,
    active BLOB not null
);
