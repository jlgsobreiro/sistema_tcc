from _models.Administrador import Administrador
from _models.Usuario import Usuario
from dao.base import BaseDao


class Administradores(BaseDao):
    def __init__(self):
        super().__init__()
        self.TABLE_NAME = 'Administradores'

    def is_admin(self, admin: Usuario):
        sql_conn = self.database_get_connection()
        query = f"select count(*) from Administradores where usuario_id = '{admin.get_id()}' AND condicao = 'ativo'"
        res = sql_conn.execute(query).fetchone()[0]
        return res != 0

    def get_admin_access_level(self, admin: Usuario):
        sql_conn = self.database_get_connection()
        query = f"select acesso from Administradores where usuario_id = '{admin.get_id()}' AND condicao = 'ativo'"
        res = sql_conn.execute(query).fetchone()
        return res[0] if res is not None else 'cliente'

    def check_access(self, admin: Usuario):
        access_level = self.get_admin_access_level(admin=admin)
        return access_level == 'total'

    def check_writeble_fields(self):
        try:
            if len(self.get_writeble_fields()) == 0:
                fields = [x for x in Administrador().__dict__.keys() if '_id' not in x]
                self.set_writeble_fields(fields=fields)
                return None
        except Exception as e:
            return e
