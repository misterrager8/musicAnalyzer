import os

import MySQLdb
from dotenv import load_dotenv

class DB:
    def __init__(self):
        load_dotenv()

    @staticmethod
    def db_read(stmt: str) -> list:
        db = MySQLdb.connect(os.getenv("host"),
                             os.getenv("user"),
                             os.getenv("passwd"),
                             os.getenv("db"))
        cursor = db.cursor()
        cursor.execute(stmt)
        return cursor.fetchall()

    @staticmethod
    def db_write(stmt: str):
        db = MySQLdb.connect(os.getenv("host"),
                             os.getenv("user"),
                             os.getenv("passwd"),
                             os.getenv("db"))
        cursor = db.cursor()
        cursor.execute(stmt)
        db.commit()

    def create(self, new_object):
        stmt = "INSERT INTO - () VALUES ()" % new_object
        self.db_write(stmt)
        print("Added.")

    def read(self):
        stmt = "SELECT * FROM -"
        self.db_read(stmt)

    def update(self, object_id):
        stmt = "UPDATE - SET - = - WHERE _id = '%d'" % object_id
        self.db_write(stmt)
        print("Updated.")

    def delete(self, object_id):
        stmt = "DELETE FROM - WHERE _id = '%d'" % object_id
        self.db_write(stmt)
        print("Deleted.")

