create table if not exists Fornecedores (
    _id integer primary key autoincrement,
    nome text unique not null ,
    endereco text,
    condicao blob not null
);
