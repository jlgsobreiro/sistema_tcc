from models.Usuario import Usuario
from repository.usuario import RepositorioUsuarios
from views.base_crud import SimpleCRUD


class UserView(SimpleCRUD):
    class Meta:
        meta = Usuario
        repo = RepositorioUsuarios

    title = 'Usuarios'


