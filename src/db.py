from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

"""数据库配置"""
HOSTNAME = "211.71.149.62"
PORT = 6636
USERNAME = 'root'
PASSWORD = '123456'
DATEBASE = 'hjw_presys'

engine = create_engine(f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATEBASE}')
DBSession = sessionmaker(bind=engine)
