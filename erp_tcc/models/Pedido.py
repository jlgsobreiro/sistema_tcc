import datetime

from api.models.Base import Base
from api.dao.clientes import Clientes
from mongoengine import Document
from mongoengine.fields import *

class Historico(Document):
    mensagem = StringField()
    data_cadastro = DateTimeField()


class ItemPedido(Document):
    produto = ObjectIdField()
    quantidade = IntField()
    total = FloatField()
    valor = FloatField()
    desconto = FloatField()


class Pedido(Document):

    cliente = ObjectIdField()
    total = FloatField()
    produtos = ListField()
    historico = ListField()
    observacoes = StringField()
    estado_atual = StringField()
    finalizado = BooleanField()

    def retorna_nome_cliente(self):
        cliente = Clientes().para_dict(str(self.cliente))
        return cliente.get('nome')

    def finalizar(self):
        self.finalizado = True

    def aberto(self):
        return not self.finalizado

    def insere_historico(self, historico: Historico):
        if self.aberto():
            self.historico.append(historico)

    def atualiza_estado_atual(self, mensagem: str):
        if self.aberto():
            if self.estado_atual is not None:
                self.insere_historico(self.estado_atual)
            self.estado_atual = Historico(mensagem=mensagem).__dict__

    def insere_produto(self, produto):
        if self.aberto():
            item_pedido = ItemPedido().from_dict(produto).__dict__
            self.produtos.append(item_pedido)
            self.calcula_total()

    def apaga_produto(self, indice):
        if self.aberto():
            self.produtos.pop(int(indice)-1)
            self.calcula_total()

    def calcula_total(self):
        total = 0
        for produto in self.produtos:
            produto['total'] = float(produto.get('valor'))*float(produto.get('quantidade'))
            total += float(produto.get('total'))
        self.total = total
