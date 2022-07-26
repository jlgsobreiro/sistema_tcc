create table if not exists Orders (
    product_id int not null ,
    quantity real not null,
    observations text,
    images blob,
    foreign key(product_id) REFERENCES Products(_id)
);
