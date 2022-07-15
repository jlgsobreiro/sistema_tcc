from _models.ShopAdmin import ShopAdmin
from _models.User import User
from dao.base import BaseDao
from dao.shops import Shops


class ShopAdmins(BaseDao):
    def __init__(self):
        super().__init__()
        self.TABLE_NAME = 'Shop_Administrators'

    def is_shop_admin(self, admin: User):
        sql_conn = self.database_get_connection()
        query = f"select count(*) from Shop_Administrators where user_id = '{admin.get_id()}' AND status = 'active'"
        res = sql_conn.execute(query).fetchone()[0]
        is_admin = True if res != 0 else False
        return is_admin

    def get_admin_shops(self, admin: User):
        sql_conn = self.database_get_connection()
        query = f"select shop_id from Shop_Administrators where user_id = '{admin.get_id()}' AND status = 'active'"
        res = sql_conn.execute(query).fetchall()
        shops = [Shops().get_shop_by_id(str(shop_id[0])) for shop_id in res]
        return shops

    def check_writeble_fields(self):
        try:
            if len(self.get_writeble_fields()) == 0:
                fields = [x for x in ShopAdmin().__dict__.keys() if '_id' not in x]
                self.set_writeble_fields(fields=fields)
                return None
        except Exception as e:
            return e
