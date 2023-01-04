from api.models.Base import Base
from mongoengine import Document
from mongoengine.fields import *


class Fornecedor(Document):
    nome = StringField()
    endereco = DictField()

    @property
    def condicao(self):
        return True

    @property
    def is_active(self):
        return self.condicao
