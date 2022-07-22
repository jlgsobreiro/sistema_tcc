from _models.Base import Base


class ShopAdmin(Base):
    def __init__(self, **kwargs):
        self.shop_id = kwargs.get('_id')
        self.user_id = kwargs.get('username')
        self.status = kwargs.get('username')

    def is_active(self):
        return self.status
