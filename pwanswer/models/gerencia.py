from mongoengine import Document, StringField

from models.base_model import BaseModel


class Gerencia(Document, BaseModel):
    COD = StringField()
    GERENCIA = StringField()

    query = '''select ADREP_CODIGO as COD, ADREP_ZONA_ATUA as GERENCIA into #gerencia from SUPADREP where ADREP_TIPO = 'R' ;'''

    def get_all(self):
        return Gerencia.objects()

    def instance_reference(self):
        return Gerencia
