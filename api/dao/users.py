import hashlib
import http

from flask import Response, jsonify

from dao.base import BaseDao
from _models.User import User
from _token.token import encode_auth_token


class Users(BaseDao):
    def register(self, user: User):
        user_values_str = (str(user.as_list()[1:])
                           .replace('[', '')
                           .replace(']', '')
                           .replace('None', 'NULL')
                           )
        user_description_str = (str([a for a in user.__dir__() if '_' not in a])
                                .replace('[', '')
                                .replace(']', '')
                                .replace("'", '')
                                )
        sql_conn = self.database_get_connection()
        try:
            sql_conn.execute("INSERT INTO Users "
                             f"({user_description_str},is_authenticated,is_active,is_anonymous) "
                             f"values ({user_values_str},FALSE, TRUE, FALSE)")
            sql_conn.commit()
            user_token = encode_auth_token(user.username)
            return {'token': user_token}
        except Exception as e:
            return {'error': e}
        finally:
            sql_conn.close()

    def login(self, username: str, password: str):
        sql_conn = self.database_get_connection()
        query = f"select * from Users where username = '{username}'"
        x = sql_conn.execute(query).fetchone()
        if x is None:
            return {'error': 'Invalid username'}
        desription = [resultado[0] for resultado in sql_conn.execute(query).description]
        dict_user = {desc: x[desription.index(desc)] for desc in desription}
        if dict_user.get('passwordHash') != hashlib.sha512(password.encode("utf-8")).hexdigest():
            return {'error': 'Invalid password'}
        return {'user': User().from_dict(dict_user), 'token': encode_auth_token(username=username)}

    def get_user_by_username(self, username: str):
        sql_conn = self.database_get_connection()
        query = f"select * from Users where '{username}' = username"
        x = sql_conn.execute(query).fetchone()
        desription = [resultado[0] for resultado in sql_conn.execute(query).description]
        dict_user = {desc: x[desription.index(desc)] for desc in desription}
        return User().from_dict(dict_user)
