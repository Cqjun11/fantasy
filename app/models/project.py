from app.models.basic import BaseModel
from sqlalchemy import String, Column, Integer, UniqueConstraint


class Project(BaseModel):
    """接口项目表"""
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    project_name = Column(String(10), nullable=True)
    owner = Column(Integer)
    project_describe = Column(String(200), nullable=False)
    __tag__ = "项目"
    __alias_ = dict(project_name="项目名称", owner="项目归属者", project_describe="项目描述")
    __table_args__ = (
        UniqueConstraint('project_name', 'deleted_at'),
    )

    def __init__(self, project_name, create_user, owner, project_describe=None):
        super().__init__(create_user)
        self.project_name = project_name
        self.owner = owner
        self.project_describe = project_describe


