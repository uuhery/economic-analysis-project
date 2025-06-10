# 如果你不使用数据库可以暂时留空或写连接池配置
# 以后可扩展 SQLAlchemy Session/Engine 等

from sqlalchemy.orm import declarative_base

Base = declarative_base()
