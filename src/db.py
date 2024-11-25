from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

"""数据库配置"""
HOSTNAME = "211.71.149.62"  # 数据库地址
PORT = 6636                 # 数据库端口
USERNAME = 'root'           # 数据库用户名
PASSWORD = '123456'         # 数据库密码
DATEBASE = 'hjw_presys'     # 数据库名称

engine = create_engine(f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATEBASE}')
DBSession = sessionmaker(bind=engine)
