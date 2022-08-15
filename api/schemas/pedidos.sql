create table if not exists Pedidos (
    usuario_id REFERENCES  Users(_id) NOT NULL ,
    produto_id REFERENCES Products(_id) NOT NULL ,
    quantidade blob not null ,
    valor_un blob not null ,
    desconto blob not null,
    total blob not null ,
    data_pedido blob not null ,
    data_baixa blob,
    condicao BLOB not null
);
