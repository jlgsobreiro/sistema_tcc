from _models.Conta import Conta
from dao.base import BaseDao


class ContasDAO(BaseDao):
    def __init__(self):
        super().__init__()
        self.TABLE_NAME = 'Contas'

    def check_writeble_fields(self):
        try:
            if len(self.get_writeble_fields()) == 0:
                fields = [x for x in Conta().__dict__.keys() if '_id' not in x]
                self.set_writeble_fields(fields=fields)
                return None
        except Exception as e:
            return e
