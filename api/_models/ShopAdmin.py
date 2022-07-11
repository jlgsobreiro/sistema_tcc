class ShopAdmin:
    def __init__(self, **kwargs):
        self.shop_id = kwargs.get('_id')
        self.user_id = kwargs.get('username')
        self.status = kwargs.get('username')

    def as_list(self):
        return [
            self.shop_id,
            self.user_id.lower(),
            self.status
        ]

    def from_dict(self, dict_user: dict):
        for key in dict_user:
            setattr(self, key, dict_user[key])
        return self

    def is_active(self):
        return self.status
