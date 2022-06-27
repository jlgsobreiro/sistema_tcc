import hashlib

from dao.base import BaseDao


class User:
    def __init__(self, **kwargs):
        self.active = True
        self._id = None
        self.username = kwargs.get('username')
        self.passwordhash = hashlib.sha512(kwargs.get('password').encode("utf-8")).hexdigest() \
            if kwargs.get('password') is not None else None
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.email = kwargs.get('email')

    def as_list(self):
        return [
            self._id,
            self.username.lower(),
            self.passwordhash,
            self.firstname,
            self.lastname,
            self.email
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
        return self

    def authenticate(self, token: str):
        sql_conn = BaseDao().database_get_connection()
        query = f"select * from Tokens where token = '{token}' AND user_id = '{self.username}'"
        res = sql_conn.execute(query).fetchone()
        sql_conn.close()
        self.is_authenticated = res is not None

    def is_authenticated(self, token: str):
        sql_conn = BaseDao().database_get_connection()
        query = f"select * from Tokens where token = '{token}' AND user_id = '{self.username}'"
        res = sql_conn.execute(query).fetchone()
        sql_conn.close()
        return res is not None

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_user_by_token(self):
        pass
