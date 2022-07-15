import hashlib
from dao.base import BaseDao
from _models.User import User


class Users(BaseDao):
    def __init__(self):
        super().__init__()
        self.TABLE_NAME = 'Users'

    def login(self, username: str, password: str):
        user = self.get_user_by_username(username=username)
        if user is None:
            return {'error': 'Invalid username'}
        if user.passwordHash != hashlib.sha512(password.encode("utf-8")).hexdigest():
            return {'error': 'Invalid password'}
        return {'user': user}

    def get_user_by_username(self, username: str):
        user = self.to_class_object(where=f"username = '{username}'", class_reference=User)
        return user

    def get_user_by_id(self, user_id: str):
        user = self.to_class_object(where=f"_id = '{user_id}'", class_reference=User)
        return user

    def update_user(self, updated_user: User):
        where = f"username = '{updated_user.username}'"
        return self.update(where=where, updated_object=updated_user, class_reference=User)

    def check_writeble_fields(self):
        try:
            if len(self.get_writeble_fields()) == 0:
                fields = [x for x in User().__dict__.keys() if '_id' not in x]
                self.set_writeble_fields(fields=fields)
                return None
        except Exception as e:
            return e
