from _models.Base import Base
from _models.Produto import Produto


class Insumos(Produto):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.insumo = kwargs.get('insumo')

