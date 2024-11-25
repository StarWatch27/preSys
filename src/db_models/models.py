from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

# 定义基类
Base = declarative_base()


class Dataset(Base):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键
    name = Column(String(128))  # 数据库名称
    abs_path = Column(String(128))  # 数据库绝对路径

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "abs_path": self.abs_path
        }


class AttackMethod(Base):
    __tablename__ = 'attack_methods'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键
    name = Column(String(128))  # 数据库名称

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class AttentionModel(Base):
    __tablename__ = 'attention_models'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键
    name = Column(String(128))  # 数据库名称
    abs_path = Column(String(128))  # 数据库绝对路径

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "abs_path": self.abs_path
        }


class AdvDataset(Base):
    __tablename__ = 'advDatasets'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键
    name = Column(String(128))  # 数据库名称
    abs_path = Column(String(128))  # 数据库绝对路径

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "abs_path": self.abs_path
        }
