from _models.Base import Base


class Lojas(Base):
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.name = kwargs.get('name')
        self.address = kwargs.get('address')
        self.active = True

    def get_id(self):
        return self._id

    def is_active(self):
        return self.active

