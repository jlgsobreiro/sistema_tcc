import hashlib

from dao.administradores import Administradores
from dao.base import BaseDao
from _models.Usuario import Usuario


class Usuarios(BaseDao):
    def __init__(self):
        super().__init__()
        self.TABLE_NAME = 'Usuarios'

    def login(self, username: str, password: str):
        user = self.get_user_by_username(usuario=username)
        if user is None:
            return {'error': 'Invalid username'}
        if user.senhaHash != hashlib.sha512(password.encode("utf-8")).hexdigest():
            return {'error': 'Invalid password'}
        return {'user': user}

    def get_user_by_username(self, usuario: str):
        user = self.to_class_object(where=f"usuario = '{usuario}'", class_reference=Usuario)
        return user

    def get_user_by_id(self, user_id: str):
        user = self.to_class_object(where=f"_id = '{user_id}'", class_reference=Usuario)
        return user

    def update_user(self, updated_user: Usuario):
        where = f"usuario = '{updated_user.usuario}'"
        return self.update(where=where, updated_object=updated_user, class_reference=Usuario)

    def is_admin(self, user: Usuario):
        return Administradores().check_access(user) is not None

    def check_access(self, user: Usuario):
        return Administradores().get_admin_access_level(user)

    def check_writeble_fields(self):
        try:
            if len(self.get_writeble_fields()) == 0:
                fields = [x for x in Usuario().__dict__.keys() if '_id' not in x]
                self.set_writeble_fields(fields=fields)
                return None
        except Exception as e:
            return e
