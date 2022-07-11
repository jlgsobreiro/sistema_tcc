class Shop:
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.name = kwargs.get('name')
        self.address = kwargs.get('address')
        self.active = True

    def as_list(self):
        return [
            self._id,
            self.name.lower(),
            self.address,
            self.active
        ]

    def get_id(self):
        return self._id

    def from_dict(self, dict_shop: dict):
        for key in dict_shop:
            setattr(self, key, dict_shop[key])
        return self

    def is_active(self):
        return self.active

