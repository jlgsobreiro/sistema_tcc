from models.Produto import Produto
from repository.produto import RepositorioProdutos
from views.base_crud import SimpleCRUD


class ProdutoView(SimpleCRUD):
    class Meta:
        meta = Produto
        repo = RepositorioProdutos

    title = 'Produtos'


