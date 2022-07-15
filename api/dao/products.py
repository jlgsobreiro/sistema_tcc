from _models.Product import Product
from dao.base import BaseDao


class Products(BaseDao):
    def __init__(self):
        super().__init__()
        self.TABLE_NAME = 'Products'

    def check_writeble_fields(self):
        try:
            if len(self.get_writeble_fields()) == 0:
                fields = [x for x in Product().__dict__.keys() if '_id' not in x]
                self.set_writeble_fields(fields=fields)
                return None
        except Exception as e:
            return e
