import requests
from requests import get

from api.models.Base import Base
from mongoengine import Document
from mongoengine.fields import *

class Loja(Document):

    cnpj = StringField()
    nome = StringField()
    ip = StringField()
    # rede = ListField()
    hash_rede = StringField()
    dados = DictField()

    @property
    def rede(self):
        return self.rede

    @rede.setter
    def rede(self, rede):
        self.rede.append([r for r in rede if r not in self.rede])
        self.hash_rede = hash(self.rede)

    def retorna_produtos(self):
        return requests.post(url=f"{self.ip}/api/produtos")

    def retorna_cliente(self, email):
        return requests.post(url=f"{self.ip}/api/cliente", json={'email': email})

    def retorna_lojas(self):
        return requests.post(url=f"{self.ip}/api/lojas")

    def atualiza_ip_publico(self):
        ip = get('https://api.ipify.org').text
        self.ip = ip

    def adiciona_cnpj(self, cnpj):
        self.cnpj = cnpj

    def adiciona_dado_especifico(self, dado: dict):
        self.dados = dado | self.dados

    @rede.setter
    def rede(self, value):
        self._rede = value
