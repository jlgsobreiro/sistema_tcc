from _models.Estoque import Estoque
from _models.Produto import Produto
from _models.Lojas import Lojas
from _models.Usuario import Usuario
from dao.base import BaseDao
from dao.estoque import Estoque
from dao.produtodao import ProdutoDAO


class Lojas(BaseDao):
    def __init__(self):
        super().__init__()
        self.TABLE_NAME = 'Lojas'

    def get_shop_by_name(self, name: str):
        shop = self.to_class_object(where=f"name = '{name}'", class_reference=Lojas)
        return shop

    def update_shop(self, updated_shop: Lojas):
        where = f"_id = '{updated_shop.get_id()}'"
        return self.update(where=where, updated_object=updated_shop, class_reference=Lojas)

    def get_inventory(self, shop: Lojas):
        where = f"shop_id = '{shop.get_id()}'"
        products = Estoque().to_list_of_class_object(where=where, class_reference=Estoque)
        products = [ProdutoDAO().to_class_object(f"_id = '{prod.product_id}'", Produto) for prod in products]
        products = [prod for prod in products if prod is not None]
        return products

    def get_shop_administrators(self, shop: Lojas):
        pass

    def add_shop_administrator(self, shop: Lojas):
        pass

    def remove_shop_administrator(self, shop: Lojas):
        pass

    def get_shop_by_id(self, shop_id):
        shop = self.to_class_object(where=f"_id = '{shop_id}'", class_reference=Lojas)
        return shop

    def check_writeble_fields(self):
        try:
            if len(self.get_writeble_fields()) == 0:
                fields = [x for x in Lojas().__dict__.keys() if '_id' not in x]
                self.set_writeble_fields(fields=fields)
                return None
        except Exception as e:
            return e
