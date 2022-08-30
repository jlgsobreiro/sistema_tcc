create table if not exists Produtos (
    _id text primary key,
    nome text not null,
    unidade text not null,
    valor real,
    custo real,
    codigo_de_barras text,
    active blob not null ,
    origem REFERENCES Fornecedores(_id)
);
