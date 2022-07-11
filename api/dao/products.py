from dao.base import BaseDao


class Products(BaseDao):
    def __init__(self):
        super().__init__()
        self.TABLE_NAME = 'Products'
