from _models.Base import Base


class Estoque(Base):
    def __init__(self, **kwargs):
        self.produto_id = kwargs.get('produto_id')
        self.loja_id = kwargs.get('loja_id')
        self.quantidade = kwargs.get('quantidade')
