from sqlalchemy.orm import relationship
from app.models import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey


class Environment(Base, BaseModel):
    """项目环境"""
    __tablename__ = 'environment'
    id = Column(Integer, primary_key=True)
    host_id = Column(Integer, ForeignKey("env_host.id"), nullable=False)
    variable_id = Column(Integer, ForeignKey("env_host.id"), nullable=False)
    env_name = Column(String(12), nullable=True)
    is_del = Column(Integer, default=1)
    env_host = relationship("Env_host", back_populates="as")
    env_variable = relationship("Env_variable", back_populates="as")


class Env_host(Base, BaseModel):
    """环境服务,负责前置url"""
    __tablename__ = "env_host"
    id = Column(Integer, primary_key=True)
    serve_name = Column(String(10), nullable=True)
    serve_url = Column(String)


class Env_variable(Base, BaseModel):
    """环境变量"""
    __tablename__ = "env_variable"
    id = Column(Integer, primary_key=True)
    var_name = Column(String)
    var_value = Column(String)
    var_describe = Column(String)
