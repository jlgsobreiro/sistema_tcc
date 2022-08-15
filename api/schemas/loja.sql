create table if not exists Loja (
    _id integer primary key autoincrement,
    nome text unique not null ,
    endereco text,
    cnpj text,
    telefone text
);
