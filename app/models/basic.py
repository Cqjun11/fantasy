from datetime import datetime
from typing import Tuple

from sqlalchemy import INT, Column, BIGINT, TIMESTAMP
from app.models import Base


class BaseModel(Base):
    id = Column(INT, primary_key=True)
    create_time = Column(TIMESTAMP, nullable=False)
    update_time = Column(TIMESTAMP, nullable=False)
    deleted_at = Column(BIGINT, nullable=False, default=0)
    create_user = Column(INT, nullable=False)
    update_user = Column(INT, nullable=False)
    __abstract__ = True
    __fields__: Tuple[Column] = [id]

    def __init__(self, user):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.create_user = user
        self.update_user = user
        self.deleted_at = 0
