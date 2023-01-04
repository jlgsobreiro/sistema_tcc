from mongoengine import Document, StringField

from models.base_model import BaseModel


class Clientes(Document, BaseModel):
    COD = StringField()
    REPRE = StringField()
    CNPJ_CPF = StringField()

    def get_all(self):
        return Clientes.objects()

    def instance_reference(self):
        return Clientes

    query = '''
                select 
                    AEMPR_CODIGO as COD,
                    AEMPR_REPR as REPRE,
                    if(AEMPR_CGC_CPF = 'F') then AEMPR_CPF ELSE AEMPR_CGC ENDIF as CNPJ_CPF 
                from SUPAEMPR where 
                    AEMPR_TIPO = 'C' AND 
                    AEMPR_STATUS = 'A' 
                    ORDER BY AEMPR_DT_CADASTRO DESC 
                '''
