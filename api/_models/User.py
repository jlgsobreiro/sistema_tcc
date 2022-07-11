import hashlib


class User:
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.username = kwargs.get('username')
        self.passwordhash = hashlib.sha512(kwargs.get('password').encode("utf-8")).hexdigest() \
            if kwargs.get('password') is not None else None
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.email = kwargs.get('email')
        self.active = True

    def as_list(self):
        return [
            self._id,
            self.username.lower(),
            self.passwordhash,
            self.firstname,
            self.lastname,
            self.email,
            self.active
        ]

    def get_id(self):
        return self._id

    def from_dict(self, dict_user: dict):
        for key in dict_user:
            setattr(self, key, dict_user[key])
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False
