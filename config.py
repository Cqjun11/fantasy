# 基础配置类
from typing import ClassVar

from pydantic_settings import BaseSettings
import os

# 获取项目根目录
root = os.path.dirname(os.path.abspath(__file__))


class BaseConfig(BaseSettings):
    log_str: ClassVar[str] = os.path.join(root, 'logs')
    log_name: ClassVar[str] = os.path.join(log_str, 'api.log')

    # 服务配置
    SERVER_HOST: ClassVar[str] = '127.0.0.1'
    SERVER_PORT: ClassVar[int] = 8000

    # 日志名
    LOG_ERROR: ClassVar[str] = "log_error"
    LOG_INFO: ClassVar[str] = "log_info"

    # 数据库配置
    MYSQL_HOST: ClassVar[str] = 'localhost'
    MYSQL_PORT: ClassVar[int] = 3306
    MYSQL_USER: ClassVar[str] = "root"
    MYSQL_PWD: ClassVar[str] = '123456'
    DBNAME: ClassVar[str] = ""

    # 异步URI
    ASYNC_SQLALCHEMY_URI: ClassVar[str] = 'mysql+aiomysql://root:123456@localhost:3306/fantasy'


mysql = 'mysql+pymysql://{}:{}@:{}:{}'.format(BaseConfig.MYSQL_USER, BaseConfig.MYSQL_PWD,
                                                                 BaseConfig.MYSQL_HOST, BaseConfig.MYSQL_PORT)
# print(mysql)
