create table if not exists Inventory (
    product_id int not null ,
    shop_id text not null,
    quantity real not null,
    foreign key(shop_id) REFERENCES Shops(_id),
    foreign key(product_id) REFERENCES Products(_id)
);
