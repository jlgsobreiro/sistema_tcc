class Inventory:
    def __init__(self, **kwargs):
        self.product_id = kwargs.get('product_id')
        self.shop_id = kwargs.get('shop_id')
        self.quantity = kwargs.get('quantity')

    def as_list(self):
        return [
            self.product_id,
            self.shop_id,
            self.quantity
        ]

    def from_dict(self, dict_inventory: dict):
        for key in dict_inventory:
            setattr(self, key, dict_inventory[key])
        return self
