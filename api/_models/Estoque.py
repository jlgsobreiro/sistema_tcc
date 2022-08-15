from _models.Base import Base


class Estoque(Base):
    def __init__(self, **kwargs):
        self.product_id = kwargs.get('product_id')
        self.shop_id = kwargs.get('shop_id')
        self.quantity = kwargs.get('quantity')
