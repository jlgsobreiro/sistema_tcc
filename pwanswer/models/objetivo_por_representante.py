from mongoengine import Document, StringField, DateTimeField, DecimalField

from models.base_model import BaseModel


class ObjetivoPorRepresentante(Document, BaseModel):
    EMPRESA = StringField()
    CLI = StringField()
    ROTA = StringField()
    ZONA = StringField()
    MERCADO = StringField()
    REPRE = StringField()
    GERENCIA = StringField()
    DT = DateTimeField()
    CX_NF = DecimalField()
    REPRE_F = StringField()

    def get_all(self):
        return ObjetivoPorRepresentante.objects()

    def instance_reference(self):
        return ObjetivoPorRepresentante

    query = '''select 
        APECD_EMPRESA as EMPRESA,
        APECD_CLIENTE as CLI,
        ROTA,
        ZONA,
        MERCADO,
        REPRE,
        '' as GERENCIA,
        cast(APECD_DATA_EMISSAO as datetime) AS DT,
        SUM(APEPC_QTD_PEDIDA) as CX_NF,
        APECD_REPRE as REPRE_F
    from VNDAPECD join VNDAPEPC ON EMPRESA = APEPC_EMPRESA AND APECD_PEDIDO = APEPC_PEDIDO
        left join BYTEC.VIEWROTAREPRESENTANTE ON CLI = CODIGO
    where APECD_DATA_EMISSAO != '00000000' AND APECD_DATA_EMISSAO > 20200000 AND APECD_DESTINO = '01' AND APEPC_DESTINO = '01' AND APEPC_STATUS != 'C'
    GROUP BY 
        DT,
        EMPRESA,
        CODIGO,
        ROTA,
        ZONA,
        MERCADO,
        APECD_CLIENTE,
        REPRE,
        REPRE_F
    order by 
        DT DESC'''
