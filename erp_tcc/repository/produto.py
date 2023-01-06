from models.Produto import Produto
from repository.base_mongo import BaseMongo


class RepositorioProdutos(BaseMongo):
    class Meta:
        model = Produto
