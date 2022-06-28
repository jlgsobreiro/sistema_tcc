import hashlib


class User:
    def __init__(self, **kwargs):
        self._id = None
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
        return self.username

    def from_dict(self, dict_user: dict):
        self._id = dict_user.get('_id')
        self.username = dict_user.get('username')
        self.passwordhash = None
        self.firstname = dict_user.get('firstname')
        self.lastname = dict_user.get('lastname')
        self.email = dict_user.get('email')
        self.active = dict_user.get('active')
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_user_by_token(self):
        pass
