from sqlalchemy import Column, Integer, String, TIMESTAMP
from datetime import datetime
from app.models import Base, BaseModel


class User(Base, BaseModel):
    """用户表"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(12), unique=True)
    password = Column(String(50), nullable=False)
    # phone = Column(String(12), unique=True)
    last_login_at = Column(TIMESTAMP)

    def __init__(self, username, password, phone=None):
        super().__init__()
        self.username = username
        self.password = password
        self.phone = phone
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


