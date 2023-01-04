from api.dao.base_mongo import BaseMongo
from api.models.Base import Base
from mongoengine import Document
from mongoengine.fields import *

meta = {'db_alias': "Administradores"}


class Administrador(BaseMongo):
    usuario_id = ObjectIdField()
    acesso = StringField()
    condicao = StringField()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.condicao

    @property
    def is_anonymous(self):
        return False
