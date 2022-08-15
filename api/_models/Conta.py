from _models.Base import Base


class Conta(Base):
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.empresa = kwargs.get('empresa')
        self.valor = kwargs.get('valor')
        self.juros = kwargs.get('juros')
        self.multa = kwargs.get('multa')
        self.data_cadastro = kwargs.get('data_cadastro')
        self.data_vencimento = kwargs.get('data_vencimento')
        self.data_baixa = kwargs.get('data_baixa')
        self.condicao = kwargs.get('status')

    def get_id(self):
        return self._id

