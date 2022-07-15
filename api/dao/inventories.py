from _models.Inventory import Inventory
from dao.base import BaseDao


class Inventories(BaseDao):
    def __init__(self):
        super().__init__()
        self.TABLE_NAME = 'Inventory'

    def check_writeble_fields(self):
        try:
            if len(self.get_writeble_fields()) == 0:
                fields = [x for x in Inventory().__dict__.keys() if 'shop_id' not in x]
                self.set_writeble_fields(fields=fields)
                return None
        except Exception as e:
            return e
