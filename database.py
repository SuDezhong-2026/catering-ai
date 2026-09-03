# database.py —— Day10：SQLAlchemy 引擎 + 会话 + 模型基类
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

# 引擎：负责连数据库。地址用 Day6 配的 settings.db_url（sqlite:///./catering.db）
engine = create_engine(settings.db_url, connect_args={"check_same_thread": False})

# 会话工厂：每次和数据库打交道，开一个"会话"（类比：打开一次数据库连接）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 所有数据库表模型都继承这个 Base，SQLAlchemy 才知道它们是表
Base = declarative_base()
# 给接口用的数据库会话依赖：每次请求开一个会话，用完自动关
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
