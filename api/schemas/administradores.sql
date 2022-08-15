create table if not exists Administradores (
    usuario_id REFERENCES Usuarios(usuario),
    acesso blob not null,
    condicao text not null
);
