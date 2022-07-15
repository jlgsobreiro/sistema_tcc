from _models.Inventory import Inventory
from _models.Product import Product
from _models.Shop import Shop
from _models.User import User
from dao.base import BaseDao
from dao.inventories import Inventories
from dao.products import Products


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
        where = f"shop_id = '{shop.get_id()}'"
        products = Inventories().to_list_of_class_object(where=where, class_reference=Inventory)
        products = [Products().to_class_object(f"_id = {prod.product_id}", Product) for prod in products]
        return products

    def get_shop_administrators(self, shop: Shop):
        pass

    def add_shop_administrator(self, shop: Shop):
        pass

    def remove_shop_administrator(self, shop: Shop):
        pass

    def get_shop_by_id(self, shop_id):
        shop = self.to_class_object(where=f"_id = '{shop_id}'", class_reference=Shop)
        return shop

    def check_writeble_fields(self):
        try:
            if len(self.get_writeble_fields()) == 0:
                fields = [x for x in Shop().__dict__.keys() if '_id' not in x]
                self.set_writeble_fields(fields=fields)
                return None
        except Exception as e:
            return e
