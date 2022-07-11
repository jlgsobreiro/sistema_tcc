from _models.Inventory import Inventory
from _models.Shop import Shop
from _models.User import User
from dao.base import BaseDao
from dao.inventories import Inventories


class Shops(BaseDao):
    def __init__(self):
        super().__init__()
        self.TABLE_NAME = 'Shops'

    def get_shop_by_name(self, name: str):
        shop = self.to_class_object(where=f"name = '{name}'", class_reference=Shop)
        return shop

    def update_shop(self, updated_shop: Shop):
        where = f"_id = '{updated_shop.get_id()}'"
        return self.update(where=where, updated_object=updated_shop, class_reference=Shop)

    def get_inventory(self, shop: Shop):
        Inventories().
        return

    def get_shop_administrators(self, shop: Shop):
        pass

    def add_shop_administrator(self, shop: Shop):
        pass

    def remove_shop_administrator(self, shop: Shop):
        pass

    def get_shop_by_id(self, shop_id):
        shop = self.to_class_object(where=f"_id = '{shop_id}'", class_reference=Shop)
        return shop
