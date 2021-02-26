from modules.base import session_factory


class DB:
    def __init__(self):
        pass

    @staticmethod
    def create(obj):
        session = session_factory()
        session.add(obj)
        session.commit()
        session.close()

    @staticmethod
    def read(obj_name):
        session = session_factory()
        results = session.query(obj_name).all()
        for i in results:
            i.to_string()

    # @staticmethod
    # def update(stmt):
    #     # session = Session()
    #     pass

    @staticmethod
    def delete(stmt):
        session = session_factory()
        session.execute(stmt)
        session.commit()
        session.close()
