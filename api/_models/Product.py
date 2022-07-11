class Product:
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.name = kwargs.get('name')
        self.unity_type = kwargs.get('unity_type')
        self.selling_price = kwargs.get('selling_price')
        self.cost_price = kwargs.get('cost_price')
        self.barcode = kwargs.get('barcode')
        self.bought_from = kwargs.get('bought_from')
        self.active = True

    def as_list(self):
        return [
            self._id,
            self.name,
            self.unity_type,
            self.selling_price,
            self.cost_price,
            self.barcode,
            self.bought_from,
            self.active
        ]

    def get_id(self):
        return self._id

    def from_dict(self, dict_product: dict):
        for key in dict_product:
            setattr(self, key, dict_product[key])
        return self

    def is_active(self):
        return self.active
