import os

import dotenv
import sqlalchemy.ext.declarative
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

db_host = os.getenv("host")
db_user = os.getenv("user")
db_passwd = os.getenv("passwd")
db_name = os.getenv("db")

engine = sqlalchemy.create_engine(f'mysql://{db_user}:{db_passwd}@{db_host}/{db_name}')
Base = sqlalchemy.ext.declarative.declarative_base()

Session = sqlalchemy.orm.sessionmaker(bind=engine)


class DB:
    def __init__(self):
        pass

    @staticmethod
    def create(obj):
        session = Session()
        session.add(obj)
        session.commit()
        session.close()

    @staticmethod
    def read(obj_name):
        session = Session()
        results = session.query(obj_name).all()
        for i in results:
            i.to_string()

    # @staticmethod
    # def update(stmt):
    #     # session = Session()
    #     pass

    @staticmethod
    def delete(stmt):
        session = Session()
        session.execute(stmt)
        session.commit()
        session.close()
