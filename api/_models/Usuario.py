import hashlib

from _models.Base import Base


class Usuario(Base):
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.usuario = kwargs.get('usuario')
        self.senhaHash = hashlib.sha512(kwargs.get('senha').encode("utf-8")).hexdigest() \
            if kwargs.get('senha') is not None else None
        self.nome = kwargs.get('nome')
        self.sobrenome = kwargs.get('sobrenome')
        self.email = kwargs.get('email')
        self.telefone = kwargs.get('telefone')
        self.condicao = True

    def get_id(self):
        return self._id

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.condicao

    def is_anonymous(self):
        return False
