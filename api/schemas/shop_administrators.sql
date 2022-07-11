create table if not exists Shop_Administrators (
    shop_id int not null,
    user_id text not null,
    status text not null,
    foreign key(user_id) REFERENCES Users(username),
    foreign key(shop_id) REFERENCES Shops(_id)
);
