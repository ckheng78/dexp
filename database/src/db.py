import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sakila.db')

class dexp_db:
    def __init__(self):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()