from sqlalchemy import Column, Integer, String, TIMESTAMP, BIGINT
from datetime import datetime
from app.models import Base


class User(Base):
    """用户表"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(12), unique=True)
    password = Column(String(50), nullable=False)
    role = Column(Integer, default=0, comment="0: 普通用户 1: 组长 2: 超级管理员")
    phone = Column(String(12), unique=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    deleted_at = Column(BIGINT, nullable=False, default=0)
    last_login_at = Column(TIMESTAMP)

    def __init__(self, username, password, phone=None):
        self.username = username
        self.password = password
        self.phone = phone
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.deleted_at = 0

