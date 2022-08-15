create table if not exists Estoque(
    produto_id REFERENCES Produtos(_id),
    loja_id REFERENCES Loja(_id),
    quantidade real not null
);
