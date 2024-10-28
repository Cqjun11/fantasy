from app.models.basic import BaseModel
from app.models import Base
from sqlalchemy import INT, Column, create_engine

from config import BaseConfig


class ProjectRole(BaseModel):
    """项目角色表"""
    __tablename__ = 'project_role'
    user_id = Column(INT, index=True)
    project_id = Column(INT, index=True)
    project_role = Column(INT, index=True)
    __alias__ = dict(user_id="用户", project_id="项目", project_role="角色")
    __tag__ = "项目角色"
    __fields__ = (project_id, user_id, project_role)

    def __init__(self, user_id: int, project_id: int, project_role: int, create_user):
        super().__init__(create_user)
        self.user_id: int = user_id
        self.project_id: int = project_id
        self.project_role: int = project_role

