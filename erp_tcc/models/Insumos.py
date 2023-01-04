from api.models.Base import Base
from api.models.Produto import Produto
from mongoengine import Document
from mongoengine.fields import *


class Insumos(Document):
    insumo = StringField()
