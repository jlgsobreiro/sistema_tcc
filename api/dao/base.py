import sqlite3


class BaseDao:
    def __init__(self):
        self.DATABASE = "api/database.db"
        self.SCHEMASQL = "api/schema.sql"

    def __initialize__(self):
        sql = self.database_get_connection()
        fp = open(self.SCHEMASQL)
        sql.execute(fp.read())
        fp.close()

    def database_get_connection(self):
        return sqlite3.connect(self.DATABASE)
