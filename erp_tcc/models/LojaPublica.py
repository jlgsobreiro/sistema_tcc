import requests
from requests import get

from api.models.Base import Base
from mongoengine import Document
from mongoengine.fields import *


class LojaPublica(Document):
    cnpj = StringField()
    nome = StringField()
    ip = StringField()
    rede = ListField()
    hash_rede = StringField()
    dados = DictField()

    def retorna_produtos(self):
        return requests.post(url=f"{self.ip}/api/produtos")

    def retorna_cliente(self, email):
        return requests.post(url=f"{self.ip}/api/cliente", json={'email': email})

    def retorna_lojas(self):
        return requests.post(url=f"{self.ip}/api/lojas")

    def retorna_hash_lojas(self):
        return requests.post(url=f"{self.ip}/api/hash_lojas")
