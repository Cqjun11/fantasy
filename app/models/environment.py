from datetime import datetime
from app.models import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP


class Environment(Base):
    """环境表"""
    __table__ = 'environment'
    id = Column(Integer, primary_key=True)
    env_name = Column(String(12), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    update_at = Column(TIMESTAMP, default=datetime.now())
    is_del = Column(Integer, default=1)

