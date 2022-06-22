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

create table if not exists Tokens (
    token text primary key,
    user_id text not null ,
    foreign key(user_id) REFERENCES Users(username)
)

