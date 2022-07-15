import sqlite3


def values_to_str_query(values_list: list):
    return (str(values_list)
            .replace('[', '')
            .replace(']', '')
            .replace('None', 'NULL')
            )


def description_to_str_query(description_list: list):
    return (str(description_list)
            .replace('[', '')
            .replace(']', '')
            .replace("'", '')
            )


class BaseDao:
    def __init__(self):
        self.TABLE_NAME = ''
        self.DATABASE = "api/database.db"
        self.SCHEMASQL = f"api/schemas/{self.TABLE_NAME.lower()}.sql"

    def __initialize__(self):
        sql = self.database_get_connection()
        fp = open(self.SCHEMASQL)
        sql.execute(fp.read())
        fp.close()

    def database_get_connection(self):
        return sqlite3.connect(self.DATABASE)

    def register(self, obj: object):
        description_list = list(obj.__dict__.keys())
        values_list = list(obj.__dict__.values())
        return self.insert_into_table(values_list=values_list, description_list=description_list)

    def insert_into_table(self, values_list: list, description_list: list):
        sql_conn = self.database_get_connection()
        try:
            sql_conn.execute(f"INSERT INTO {self.TABLE_NAME} "
                             f"({description_to_str_query(description_list)}) "
                             f"values ({values_to_str_query(values_list)})")
            return {'message': "Success"}
        except Exception as e:
            sql_conn.rollback()
            return {'error': e}
        finally:
            sql_conn.commit()
            sql_conn.close()

    def get_table_description(self):
        sql_conn = self.database_get_connection()
        query = f"select * from {self.TABLE_NAME}"
        description = [resultado[0] for resultado in sql_conn.execute(query).description]
        sql_conn.close()
        return description

    def to_class_object(self, where: str, class_reference: object):
        sql_conn = self.database_get_connection()
        description = self.get_table_description()
        query = f"select * from {self.TABLE_NAME} where {where};"
        x = sql_conn.execute(query).fetchone()
        if x is None:
            sql_conn.close()
            return None
        to_dict = {desc: x[description.index(desc)] for desc in description}
        sql_conn.close()
        return class_reference().from_dict(to_dict)

    def to_list_of_class_object(self, where: str, class_reference: object):
        sql_conn = self.database_get_connection()
        description = self.get_table_description()
        if where == '' or where is None:
            where = ''
        else:
            where = f'where {where}'
        query = f"select * from {self.TABLE_NAME} {where};"
        x = sql_conn.execute(query).fetchall()
        if x is None:
            sql_conn.close()
            return None
        list_objects = []
        for item in x:
            list_objects.append(
                class_reference().from_dict({desc: item[description.index(desc)] for desc in description}))
        sql_conn.close()
        return list_objects

    def update(self, where: str, updated_object, class_reference: object):
        object_to_update = self.to_class_object(where=where, class_reference=class_reference)
        if updated_object == object_to_update:
            return None
        values = []
        for key in updated_object.__dict__:
            if updated_object.__dict__[key] != object_to_update.__dict__[key]:
                values.append(f"{key} = '{updated_object.__dict__[key]}'")
        values = ','.join(x for x in values)
        sql_conn = self.database_get_connection()
        try:
            query = f"Update {self.TABLE_NAME} set {values} where {where}"
            sql_conn.execute(query)
            sql_conn.commit()
            return {'Update': 'Success'}
        except Exception as e:
            sql_conn.rollback()
            return {'error': e}
        finally:
            sql_conn.close()

    def get_count(self, where: str):
        sql_conn = self.database_get_connection()
        where = f"where {where}" if where != '' else ''
        try:
            query = f"select count(*) from {self.TABLE_NAME} {where}"
            count = sql_conn.execute(query).fetchone()
            return count[0]
        except Exception as e:
            return {'error': e}
        finally:
            sql_conn.close()

    def get_writeble_fields(self):
        sql_conn = self.database_get_connection()
        fields = sql_conn.execute(
            f"select field_name from Writeble_Fields where table_name = '{self.TABLE_NAME}'").fetchall()
        sql_conn.close()
        return fields

    def set_writeble_fields(self, fields: list):
        sql_conn = self.database_get_connection()
        try:
            for field in fields:
                sql_conn.execute(
                    f"INSERT INTO Writeble_Fields (table_name, field_name) values ('{self.TABLE_NAME}','{field}')")
            sql_conn.commit()
        except Exception as e:
            sql_conn.rollback()
            return {'error': e}
        finally:
            sql_conn.close()


