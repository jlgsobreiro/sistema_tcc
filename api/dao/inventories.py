from dao.base import BaseDao


class Inventories(BaseDao):
    def __init__(self):
        super().__init__()
        self.TABLE_NAME = 'Inventory'
