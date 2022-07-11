create table if not exists Products (
    _id integer primary key autoincrement,
    name text not null,
    unity_type text not null,
    selling_price real,
    cost_price real,
    barcode text,
    active blob not null ,
    bought_from int,
    foreign key (bought_from) REFERENCES Shops(_id)
);
