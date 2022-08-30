from _models.Produto import Produto
from dao.base import BaseDao


class ProdutoDAO(BaseDao):
    def __init__(self):
        super().__init__()
        self.TABLE_NAME = 'Produtos'

    def check_writeble_fields(self):
        try:
            if len(self.get_writeble_fields()) == 0:
                fields = [x for x in Produto().__dict__.keys() if '_id' not in x]
                self.set_writeble_fields(fields=fields)
                return None
        except Exception as e:
            return e
