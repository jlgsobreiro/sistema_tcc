import hashlib

from _models.Base import Base


class User(Base):
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.username = kwargs.get('username')
        self.passwordHash = hashlib.sha512(kwargs.get('password').encode("utf-8")).hexdigest() \
            if kwargs.get('password') is not None else None
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.email = kwargs.get('email')
        self.active = True

    def get_id(self):
        return self._id

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False
