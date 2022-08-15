from _models.Base import Base


class Fornecedor(Base):
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.nome = kwargs.get('nome')
        self.endereco = kwargs.get('endereco')
        self.condicao = True

    def get_id(self):
        return self._id

    def is_active(self):
        return self.condicao

