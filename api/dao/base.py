import os
import sqlite3
import sys


class BaseDao:
    def __init__(self):
        self.DATABASE = "C:\\Users\\jl_so\\Documents\\sisteminha2\\api\\database.db"
        self.SCHEMASQL = "C:\\Users\\jl_so\\Documents\\sisteminha2\\api\\schema.sql"

    def __initialize__(self):
        sql = self.database_get_connection()
        fp = open(self.SCHEMASQL)
        sql.execute(fp.read())
        fp.close()

    def database_get_connection(self):
        return sqlite3.connect(self.DATABASE)
