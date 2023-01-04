from mongoengine import Document, StringField, DecimalField, DateTimeField

from models.base_model import BaseModel


class Cobrancas(Document, BaseModel):
    REPR = StringField()
    ROTA = StringField()
    ST = StringField()
    CLI = StringField()
    FANTASIA = StringField()
    RAZAO_SOCIAL = StringField()
    CIDADE = StringField()
    BAIRRO = StringField()
    ENDERECO = StringField()
    CEP = DecimalField()
    CONTATO_1 = StringField()
    CELULAR_1 = StringField()
    TELEFONE_1 = StringField()
    CONTATO_2 = StringField()
    CELULAR_2 = StringField()
    TELEFONE_2 = StringField()
    EMP = StringField()
    NOTA = StringField()
    BANCO = StringField()
    EMISSAO = DateTimeField()
    VCTO = DateTimeField()
    D_VNC = DecimalField()
    PARC = StringField()
    VALOR = DecimalField()

    def get_all(self):
        return Cobrancas.objects()

    def instance_reference(self):
        return Cobrancas

    query = '''
        SELECT 
    mpr.AEMPR_REPR AS REPR,
    nte.ROTA as ROTA,
    mpr.AEMPR_STATUS as ST,
    fcd.ANFCD_CLIENTE AS CLI,
    mpr.AEMPR_NOME_ABREV AS FANTASIA,
    mpr.AEMPR_RAZAO_SOCIAL AS RAZAO_SOCIAL,
    nte.CIDADE,
    nte.BAIRRO,
    nte.ENDERECO,
    nte.CEP,
    mpr.AEMPR_NOME_CONT1 AS CONTATO_1,
    mpr.AEMPR_TELEX_CONT1 AS CELULAR_1,
    mpr.AEMPR_FONE_CONT1 AS TELEFONE_1,
    mpr.AEMPR_NOME_CONT2 AS CONTATO_2,
    mpr.AEMPR_TELEX_CONT2 AS CELULAR_2,
    mpr.AEMPR_FONE_CONT2 AS TELEFONE_2,
    fcd.ANFCD_EMPRESA AS EMP,
    fcd.ANFCD_NUM_NOTA AS NOTA,
    lar.BancoCobranca as BANCO,
    cast(fcd.ANFCD_DATA_EMISSAO as DATETIME) AS EMISSAO, 
    cast(lar.VENCIMENTO as datetime) AS VCTO, 
    datediff(day,lar.Vencimento,now()) as D_VNC,
    lar.PARCELA as PARC,
    lar.VALOR
FROM 
    SUPAEMPR mpr,
    VNDANFCD fcd,
    VNDAEMDF mdf,
    PARCELAR lar,
    BYTEC2.VIEWROTAREPRESENTANTE nte
where
    fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND
    fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND
    fcd.ANFCD_CLIENTE = nte.CODIGO AND
    fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND
    fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND
    fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND
    fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND
    fcd.ANFCD_TIPO_EMPR = 'C' AND
    SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND
    lar.RECEBIMENTO IS NULL AND 
    lar.VENCIMENTO+1 <= now()
EXCEPT (
SELECT 
    mpr.AEMPR_REPR AS REPR,
    nte.ROTA as ROTA,
    mpr.AEMPR_STATUS as ST,
    fcd.ANFCD_CLIENTE AS CLI,
    mpr.AEMPR_NOME_ABREV AS FANTASIA,
    mpr.AEMPR_RAZAO_SOCIAL AS RAZAO_SOCIAL,
    nte.CIDADE,
    nte.BAIRRO,
    nte.ENDERECO,
    nte.CEP,
    mpr.AEMPR_NOME_CONT1 AS CONTATO_1,
    mpr.AEMPR_TELEX_CONT1 AS CELULAR_1,
    mpr.AEMPR_FONE_CONT1 AS TELEFONE_1,
    mpr.AEMPR_NOME_CONT2 AS CONTATO_2,
    mpr.AEMPR_TELEX_CONT2 AS CELULAR_2,
    mpr.AEMPR_FONE_CONT2 AS TELEFONE_2,
    fcd.ANFCD_EMPRESA AS EMP,
    fcd.ANFCD_NUM_NOTA AS NOTA,
    lar.BancoCobranca as BANCO,
    cast(fcd.ANFCD_DATA_EMISSAO as DATETIME) AS EMISSAO, 
    cast(lar.VENCIMENTO as datetime) AS VCTO, 
    datediff(day,lar.Vencimento,now()) as D_VNC,
    lar.PARCELA as PARC,
    lar.VALOR
FROM 
    SUPAEMPR mpr,
    VNDANFCD fcd,
    VNDAEMDF mdf,
    PARCELAR lar,
    BYTEC2.VIEWROTAREPRESENTANTE nte
where
    fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND
    fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND
    fcd.ANFCD_CLIENTE = nte.CODIGO AND
    fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND
    fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND
    fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND
    fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND
    fcd.ANFCD_TIPO_EMPR = 'C' AND
    SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND
    lar.RECEBIMENTO IS NULL AND 
    lar.VENCIMENTO+1 <= now() AND 
    lar.Vencimento = fcd.ANFCD_DATA_EMISSAO AND 
    datediff(day,lar.Vencimento,now()) <= 2
)
        '''
