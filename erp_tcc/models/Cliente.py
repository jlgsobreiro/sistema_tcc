import hashlib

from api.models.Base import Base
from mongoengine import Document
from mongoengine.fields import *


class Cliente(Document):
    usuario = StringField()
    senhaHash = StringField()
    cpf_cnpj = StringField()
    nome = StringField()
    sobrenome = StringField()
    telefone = StringField()
    ativo = BooleanField()
    bairro = StringField()
    cep = StringField()
    cidade = StringField()
    numero = StringField()
    referencia = StringField()
    rua = StringField()
    uf = StringField()
    email = StringField()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.ativo

    @property
    def is_anonymous(self):
        return False
