from sqlalchemy import text

from musicAnalyzer import db


class Database:
    def __init__(self):
        pass

    @staticmethod
    def add(object_):
        db.session.add(object_)
        db.session.commit()

    @staticmethod
    def add_multiple(objects: list):
        for i in objects: db.session.add(i)
        db.session.commit()

    @staticmethod
    def get(type_, id_: int):
        return db.session.query(type_).get(id_)

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(object_):
        db.session.delete(object_)
        db.session.commit()

    @staticmethod
    def delete_multiple(objects: list):
        for i in objects: db.session.delete(i)
        db.session.commit()

    @staticmethod
    def search(type_, filter_: str = "", order_by: str = ""):
        return db.session.query(type_).filter(text(filter_)).order_by(text(order_by))

    @staticmethod
    def execute_stmt(stmt: str):
        db.session.execute(stmt)
        db.session.commit()
