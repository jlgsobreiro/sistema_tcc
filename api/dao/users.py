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
            sql_conn.close()
            return {'error': 'Invalid username'}
        desription = [resultado[0] for resultado in sql_conn.execute(query).description]
        dict_user = {desc: x[desription.index(desc)] for desc in desription}
        sql_conn.close()
        if dict_user.get('passwordHash') != hashlib.sha512(password.encode("utf-8")).hexdigest():
            return {'error': 'Invalid password'}
        token = encode_auth_token(username=username)
        self.register_token(token=token, username=username)
        return {'user': User().from_dict(dict_user), 'token': token}

    def get_user_by_username(self, username: str, token: str):
        sql_conn = self.database_get_connection()
        query = f"select * from Users where '{username}' = username"
        x = sql_conn.execute(query).fetchone()
        desription = [resultado[0] for resultado in sql_conn.execute(query).description]
        dict_user = {desc: x[desription.index(desc)] for desc in desription}
        sql_conn.close()
        return User(token=token).from_dict(dict_user)

    def register_token(self, token: str, username: str):
        sql_conn = self.database_get_connection()
        query = f"Insert into Tokens values ('{token}','{username}')"
        sql_conn.execute(query)
        sql_conn.commit()
        sql_conn.close()

    def get_tokens(self, username: str):
        sql_conn = self.database_get_connection()
        query = f"select * from Tokens where user_id = '{username}')"
        res = sql_conn.execute(query).fetchall()
        sql_conn.close()
        return res

    def del_tokens(self, username: str, token: str):
        sql_conn = self.database_get_connection()
        query = f"delete from Tokens where user_id = '{username}' AND token = '{token}')"
        res = sql_conn.execute(query).fetchone()
        sql_conn.commit()
        sql_conn.close()
        return res

    def check_token(self, token: str, username: str):
        sql_conn = self.database_get_connection()
        query = f"select * from Tokens where token = '{token}' AND user_id = '{username}')"
        res = sql_conn.execute(query).fetchone()
        sql_conn.close()
        return res is not None
