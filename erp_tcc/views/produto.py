from flask.views import MethodView

from models.Produto import Produto
from models.Usuario import Usuario
from repository.usuario import RepositorioUsuarios
from views.base_crud import SimpleCRUD


class ProdutoView(MethodView, SimpleCRUD):
    class Meta:
        meta = Produto

    title = 'Produtos'


