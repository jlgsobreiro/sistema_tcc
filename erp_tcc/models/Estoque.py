from api.models.Base import Base
from mongoengine import Document
from mongoengine.fields import *


class Estoque(Document):
    produto_id = ObjectIdField()
    loja_id = ObjectIdField()
    quantidade = IntField()
    data_entrada = DateTimeField()
    data_vencimento = DateTimeField()
