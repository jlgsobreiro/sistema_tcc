from _models.Base import Base


class Produto(Base):
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.nome = kwargs.get('nome')
        self.unidade = kwargs.get('unidade')
        self.valor = kwargs.get('valor')
        self.custo = kwargs.get('custo')
        self.codigo_de_barras = kwargs.get('codigo_de_barras')
        self.origem = kwargs.get('origem')
        self.insumo = kwargs.get('insumo')
        self.active = True

    def get_id(self):
        return self._id

    def is_active(self):
        return self.active
