from src.db import DBSession
from src.db_models.models import AttentionModel


class AttentionModelService:
    def __init__(self):
        self.db_session = DBSession()

    def add(self, name, abs_path):
        try:
            data = AttentionModel(name=str(name), abs_path=str(abs_path))
            print(data.to_dict())
            self.db_session.add(data)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            print(e)
            return False
        return True

    def get_by_id(self, id) -> AttentionModel:
        data = self.db_session.query(AttentionModel).filter_by(id=id).one()
        return data

    def edit_by_id(self, id, name, abs_path):
        try:
            data = self.db_session.query(AttentionModel).filter_by(id=id).one()
            data.name = str(name)
            data.abs_path = str(abs_path)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            print(e)
            return False
        return True

    def get_all(self) -> list[AttentionModel]:
        data_list = self.db_session.query(AttentionModel).all()
        data_list = [data.to_dict() for data in data_list]
        return data_list

    def delete_by_id(self, id):
        try:
            data = self.db_session.query(AttentionModel).filter_by(id=id).one()
            self.db_session.delete(data)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            print(e)
            return False
        return True
