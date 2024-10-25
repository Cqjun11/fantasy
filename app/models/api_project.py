from app.models import Base, BaseModel
from sqlalchemy import String, Column, Integer, TIMESTAMP
from datetime import datetime


class Api_project(Base, BaseModel):
    """接口项目表"""
    __tablename__ = 'api_project'
    id = Column(Integer, primary_key=True)
    p_name = Column(String(10), nullable=True)
    owner = Column(String(10), nullable=True)
    p_describe = Column(String(20), nullable=False)
    __tag__ = "接口项目"
    __alias_ = dict(name="项目名称", owner="项目归属者", p_describe="项目描述")

    def __init__(self, name, owner, p_describe=None):
        super().__init__()
        self.name = name
        self.owner = owner
        self.p_describe = p_describe
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
