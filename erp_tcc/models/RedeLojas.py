from api.models.Base import Base
from mongoengine import Document
from mongoengine.fields import *


class Lojas(Document):
    name = StringField()
    address = DictField()
    active = BooleanField()

    @property
    def active(self):
        return True

    @property
    def is_active(self):
        return self.active
