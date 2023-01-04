from mongoengine import Document
from mongoengine.fields import *


class Produto(Document):
    nome = StringField()
    unidade = IntField()
    valor = FloatField()
    custo = FloatField()
    codigo_de_barras = StringField()
    origem = StringField()
    quantidade = StringField()
    imagem_url = StringField()

    @property
    def active(self):
        return True

    def adiciona_imagem(self, imagem_url):
        self.imagem_url.append(imagem_url)

    def is_active(self):
        return self.active
