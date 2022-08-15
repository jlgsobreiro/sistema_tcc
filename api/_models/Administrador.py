from _models.Base import Base


class Administrador(Base):
    def __init__(self, **kwargs):
        self.usuario_id = kwargs.get('usuario_id')
        self.acesso = kwargs.get('acesso')
        self.condicao = kwargs.get('condicao')

    def is_active(self):
        return self.condicao
