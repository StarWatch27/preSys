from src.db import DBSession
from src.db_models.models import AttackMethod


class AttackMethodService:
    def __init__(self):
        self.db_session = DBSession()

    def add(self, name):
        print(f"name: {name}")
        try:
            data = AttackMethod(name=str(name))
            print(data.to_dict())
            self.db_session.add(data)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            print(e)
            return False
        return True

    def get_by_id(self, id) -> AttackMethod:
        data = self.db_session.query(AttackMethod).filter_by(id=id).one()
        return data

    def edit_by_id(self, id, name):
        try:
            data = self.db_session.query(AttackMethod).filter_by(id=id).one()
            data.name = str(name)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            print(e)
            return False
        return True

    def get_all(self) -> list[AttackMethod]:
        data_list = self.db_session.query(AttackMethod).all()
        data_list = [data.to_dict() for data in data_list]
        return data_list

    def delete_by_id(self, id):
        try:
            data = self.db_session.query(AttackMethod).filter_by(id=id).one()
            self.db_session.delete(data)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            print(e)
            return False
        return True
