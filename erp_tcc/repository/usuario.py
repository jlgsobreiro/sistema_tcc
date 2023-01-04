from models.Usuario import Usuario
from repository.base_mongo import BaseMongo


class RepositorioUsuarios(BaseMongo):
    class Meta:
        model = Usuario
