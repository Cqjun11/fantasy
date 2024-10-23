from app.models import Base
from sqlalchemy import String, Column, Integer, TIMESTAMP
from datetime import datetime


class Api_project(Base):
    """接口项目表"""
    __table__ = 'api_project'
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=True)
    create_at = Column(TIMESTAMP, nullable=True, default=datetime.now())
    update_at = Column(TIMESTAMP, default=datetime.now())
    is_del = Column(Integer, default=1)

    def __init__(self, name):
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
