from bson import ObjectId
from mongoengine import Document
from mongoengine.fields import *

from models.BaseModel import BaseModel


class Usuario(Document, BaseModel):
    usuario = StringField(required=True)
    senha = StringField(required=True)
    nome = StringField(required=True)
    sobrenome = StringField(required=True)
    email = EmailField(required=True)
    telefone = StringField(required=True)

    def get_all(self):
        return Usuario.objects()

    def instance_reference(self):
        return Usuario

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return ObjectId(self.id).__str__()
