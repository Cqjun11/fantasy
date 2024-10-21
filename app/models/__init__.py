from sqlalchemy import create_engine, sql
from asyncio import current_task
from sqlalchemy.ext.asyncio import create_async_engine, async_scoped_session, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from config import BaseConfig


def create_database():
    """创建数据库"""
    engine = create_engine('mysql+pymysql://{}:{}@{}:{}'.format(BaseConfig.MYSQL_USER, BaseConfig.MYSQL_PWD,
                                                                BaseConfig.MYSQL_HOST, BaseConfig.MYSQL_PORT),
                           echo=True)
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(
                sql.text(
                    "CREATE DATABASE IF NOT EXISTS Fantasy default character set utf8mb4 COLLATE utf8mb4_unicode_ci"))
    # close engine
    engine.dispose()


# 建库
create_database()
# # 异步创建数据库连接
async_engine = create_async_engine(
    BaseConfig.ASYNC_SQLALCHEMY_URI,
    max_overflow=0,
    pool_size=50,
    pool_recycle=1500
)

async_session_factory = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async_session = async_scoped_session(async_session_factory, scopefunc=current_task)

# 创建对象的基类:
Base = declarative_base()


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
