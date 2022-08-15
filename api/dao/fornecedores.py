from _models.Fornecedor import Fornecedor
from _models.ShopAdmin import ShopAdmin
from _models.Usuario import Usuario
from dao.base import BaseDao
from dao.lojas import Lojas


class FornecedoresDAO(BaseDao):
    def __init__(self):
        super().__init__()
        self.TABLE_NAME = 'Fornecedores'

    def lista_fornecedores(self):
        sql_conn = self.database_get_connection()
        query = f"select nome from Fornecedores"
        res = sql_conn.execute(query).fetchall()
        fornecedores = [nome[0] for nome in res]
        return fornecedores

    def check_writeble_fields(self):
        try:
            if len(self.get_writeble_fields()) == 0:
                fields = [x for x in Fornecedor().__dict__.keys() if '_id' not in x]
                self.set_writeble_fields(fields=fields)
                return None
        except Exception as e:
            return e
