import pyodbc


class BaseModel:

    def __init__(self):
        self.query = ''

    def get_all(self):
        raise Exception('Implementar função')

    def instance_reference(self):
        raise Exception('Implementar função')

    def get_connection(self):
        return pyodbc.connect(Dsn="PW64", uid="BYTEC", pwd="BYTEC")

    def get_sql(self, query):
        return self.get_connection().execute(query)

    def update_sql_reference(self):
        self.save_from_sql_list(self.get_sql(self.query))
        return self

    def wipe_and_repopulate(self):
        try:
            sql_cursor = self.get_sql(self.query)
            self.instance_reference().objects.delete()
            for cursor in sql_cursor:
                print(cursor)
                new_object = self.instance_reference()().from_sql_to_self(cursor)
                new_object.save()
        except Exception as e:
            raise f"Error ocorrido: {e}"

    def to_dict(self):
        to_dict = {}
        for value in self:
            if value != 'id':
                to_dict[value] = getattr(self, value)
        return to_dict

    def get_all_to_dict_list(self):
        return [x.to_dict() for x in self.get_all()]

    def sql_cursor_to_dict_list(self, sql_cursor):
        return [self.from_sql_to_dict(x) for x in sql_cursor]

    def save_from_sql_list(self, sql_cursor):
        objects_hash_from_mongo = [hash(x.__str__()) for x in self.get_all_to_dict_list()]
        objects_from_sql = [(hash(x.__str__()), x) for x in self.sql_cursor_to_dict_list(sql_cursor)]
        for hash_sql_object, sql_object_dict in objects_from_sql:
            print(hash_sql_object, sql_object_dict)
            print(hash_sql_object not in objects_hash_from_mongo)
            if hash_sql_object not in objects_hash_from_mongo:
                self.save_object_from_dict(sql_object_dict)

    def save_from_sql(self, sql_object):
        if not self.compare_is_equal_from_sql(sql_object):
            self.from_sql_to_self(sql_object)
            self.save()

    def save_object_from_dict(self, sql_dict):
            self.from_dict_to_self(sql_dict)
            self.save()

    def from_sql_to_self(self, sql_object):
        for key in sql_object.cursor_description:
            setattr(self, key[0], getattr(sql_object, key[0]))
        return self

    def from_dict_to_self(self, sql_dict: dict):
        for key in sql_dict.keys():
            setattr(self, key, sql_dict[key])
        return self

    def from_sql_to_dict(self, sql_object):
        dict_sql_object = {}
        for key in sql_object.cursor_description:
            dict_sql_object[key[0]] = getattr(sql_object, key[0])
        return dict_sql_object

    def compare_is_equal_from_sql(self, sql_object):
        x = self.from_sql_to_dict(sql_object)
        return self.to_dict() == x

    def create_table(self):
        if not self.get_all():
            return ''
        list_document = [item.to_dict() for item in self.get_all()]
        keys = list_document[0].keys()
        keys_string = ''
        for key in keys:
            keys_string += f'<th>{key}</th>'

        rows_string = ''
        for row in list_document:
            rows_string += '<tr>'
            for value in row:
                rows_string += f'<td>{row[value]}</td>'
            rows_string += '</tr>'

        thead_string = f'<thead><tr>{keys_string}</tr></thead>'
        tbody_string = f'<tbody>{rows_string}</tbody>'
        table_string = f'<table>{thead_string}{tbody_string}</table>'
        return f'<html>{table_string}</html>'
