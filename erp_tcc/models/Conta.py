from api.models.Base import Base
from mongoengine import Document
from mongoengine.fields import *


class Conta(Document):
    empresa = ObjectIdField()
    valor = FloatField()
    juros = FloatField()
    multa = FloatField()
    data_cadastro = DateTimeField()
    data_vencimento = DateTimeField()
    data_baixa = DateTimeField()
    condicao = BooleanField()
