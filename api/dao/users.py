import hashlib
from dao.base import BaseDao
from _models.User import User


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
                             f"({user_description_str}) "
                             f"values ({user_values_str})")
            sql_conn.commit()
            user_token = encode_auth_token(user.username)
            return {'token': user_token}
        except Exception as e:
            return {'error': e}
        finally:
            sql_conn.close()

    def get_table_users_description(self):
        sql_conn = self.database_get_connection()
        query = f"select * from Users"
        description = [resultado[0] for resultado in sql_conn.execute(query).description]
        sql_conn.close()
        return description

    def user_to_dict(self, username: str):
        sql_conn = self.database_get_connection()
        description = self.get_table_users_description()
        query = f"select * from Users where username = '{username}'"
        x = sql_conn.execute(query).fetchone()
        if x is None:
            sql_conn.close()
            return None
        dict_user = {desc: x[description.index(desc)] for desc in description}
        sql_conn.close()
        return dict_user

    def user_object_to_dict(self, user: User):
        if user is None:
            return None
        description = self.get_table_users_description()
        dict_user = {desc: user.as_list()[description.index(desc)] for desc in description}
        return dict_user

    def login(self, username: str, password: str):
        dict_user = self.user_to_dict(username=username)
        if dict_user is None:
            return {'error': 'Invalid username'}
        if dict_user.get('passwordHash') != hashlib.sha512(password.encode("utf-8")).hexdigest():
            return {'error': 'Invalid password'}
        #token = encode_auth_token(username=username)
        #self.register_token(token=token, username=username)
        return {'user': User().from_dict(dict_user)}

    def get_user_by_username(self, username: str):
        dict_user = self.user_to_dict(username=username)
        return User(username=username).from_dict(dict_user) if dict_user is not None else None

    def update_user(self, user: User):
        sql_conn = self.database_get_connection()
        updated_user = self.user_object_to_dict(user)
        user_to_update = self.user_to_dict(username=user.username)
        if updated_user == user_to_update:
            return None
        values = []
        if updated_user.get('firstname') != user_to_update.get('firstname'):
            values.append(f"firstname = '{updated_user.get('firstname')}'")
        if updated_user.get('lastname') != user_to_update.get('lastname'):
            values.append(f"lastname = '{updated_user.get('lastname')}'")
        if updated_user.get('email') != user_to_update.get('email'):
            values.append(f"email = '{updated_user.get('email')}'")
        values = ','.join(x for x in values)
        query = f"Update Users set {values} where username = '{user_to_update.get('username')}'"
        sql_conn.execute(query)
        sql_conn.commit()
        sql_conn.close()

