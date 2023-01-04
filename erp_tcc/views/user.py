from flask.views import MethodView

from models.Usuario import Usuario
from repository.usuario import RepositorioUsuarios
from views.base_crud import SimpleCRUD


class UserView(MethodView, SimpleCRUD):
    class Meta:
        meta = Usuario



    title = 'Usuarios'


