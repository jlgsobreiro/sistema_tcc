create table if not exists Photos (
    _id primary key,
    product_id REFERENCES Products(_id) ,
    url text not null
);
