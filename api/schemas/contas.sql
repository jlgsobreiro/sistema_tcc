create table if not exists Contas (
    _id text primary key,
    empresa not null foreign key REFERENCES Fornecedores(_id),
    valor blob not null,
    juros blob,
    multa blob,
    data_cadastro blob not null ,
    data_vencimento blob not null ,
    data_baixa BLOB ,
    condicao text not null
);
