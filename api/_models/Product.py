from _models.Base import Base


class Product(Base):
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.name = kwargs.get('name')
        self.unity_type = kwargs.get('unity_type')
        self.selling_price = kwargs.get('selling_price')
        self.cost_price = kwargs.get('cost_price')
        self.barcode = kwargs.get('barcode')
        self.bought_from = kwargs.get('bought_from')
        self.active = True

    def get_id(self):
        return self._id

    def is_active(self):
        return self.active
