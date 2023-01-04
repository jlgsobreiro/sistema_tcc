from mongoengine import Document
from mongoengine.fields import *
class ShopAdmin(Document):

    shop_id = StringField()
    user_id = StringField()
    status = StringField()

    def is_active(self):
        return self.status
