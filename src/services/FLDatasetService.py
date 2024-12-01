from src.db import DBSession
from src.db_models.models import FLDataset


class FLDatasetService:
    def __init__(self):
        self.db_session = DBSession()
    #
    # def add(self, name, abs_path):
    #     print(f"adding... name: {name}, abs_path: {abs_path}")
    #     try:
    #         data = FLDataset(name=str(name), abs_path=str(abs_path))
    #         print(data.to_dict())
    #         self.db_session.add(data)
    #         self.db_session.commit()
    #     except Exception as e:
    #         self.db_session.rollback()
    #         print(e)
    #         return False
    #     return True
    #
    # def edit_by_id(self, id, name, abs_path):
    #     print(f"editing... name: {name}, abs_path: {abs_path}")
    #     try:
    #         data = self.db_session.query(FLDataset).filter_by(id=id).one()
    #         data.name = str(name)
    #         data.abs_path = str(abs_path)
    #         self.db_session.commit()
    #     except Exception as e:
    #         self.db_session.rollback()
    #         print(e)
    #         return False
    #     return True
    #
    # def get_by_id(self, id) -> FLDataset:
    #     data = self.db_session.query(FLDataset).filter_by(id=id).one()
    #     return data
    #
    def get_all(self) -> list[FLDataset]:
        data_list = self.db_session.query(FLDataset).all()
        data_list = [data.to_dict() for data in data_list]
        return data_list
    #
    # def delete_by_id(self, id):
    #     try:
    #         data = self.db_session.query(FLDataset).filter_by(id=id).one()
    #         self.db_session.delete(data)
    #         self.db_session.commit()
    #     except Exception as e:
    #         self.db_session.rollback()
    #         print(e)
    #         return False
    #     return True

    def clear_table(self):
        """
        使用DELETE语句清空Dataset表中的所有数据
        """
        try:
            # 执行DELETE语句来删除所有行
            self.db_session.execute(FLDataset.__table__.delete())
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            print(e)
            return False
        return True
