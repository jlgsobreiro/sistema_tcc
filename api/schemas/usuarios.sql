create table if not exists Usuarios (
    _id text primary key,
    usuario text not null unique,
    senhaHash blob not null,
    nome text not null ,
    sobrenome text not null ,
    email text unique not null ,
    telefone text,
    condicao BLOB not null
);
