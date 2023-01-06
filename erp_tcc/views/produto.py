from flask.views import MethodView

from models.Produto import Produto
from models.Usuario import Usuario
from repository.produto import RepositorioProdutos
from repository.usuario import RepositorioUsuarios
from views.base_crud import SimpleCRUD


class ProdutoView(SimpleCRUD):
    class Meta:
        meta = Produto
        repo = RepositorioProdutos

    title = 'Produtos'


