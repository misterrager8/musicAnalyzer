import os

import MySQLdb
from dotenv import load_dotenv
from sqlalchemy import create_engine


class DB:
    def __init__(self):
        load_dotenv()
        db_host = os.getenv("host")
        db_user = os.getenv("user")
        db_passwd = os.getenv("passwd")
        db_name = os.getenv("db")

        self.db = create_engine(f'mysql://{db_user}:{db_passwd}@{db_host}/{db_name}')

    def read(self, stmt: str) -> list:
        try:
            cursor = self.db.cursor()
            cursor.execute(stmt)
            return cursor.fetchall()
        except MySQLdb.Error as e:
            print(e)

    def write(self, stmt: str):
        try:
            cursor = self.db.cursor()
            cursor.execute(stmt)
            self.db.commit()
        except MySQLdb.Error as e:
            print(e)
