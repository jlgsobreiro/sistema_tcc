create table if not exists Shops (
    _id integer primary key autoincrement,
    name text unique not null ,
    address text,
    active blob not null
);
