from pydantic import BaseModel, field_validator

from app.enums.RequestBodyEnum import BodyType


class HttpRequestForm(BaseModel):
    method: str
    url: str
    body: str = None
    headers: dict = {}
    body_type: BodyType = BodyType.none

    @field_validator("method", 'url')
    def name_not_empty(cls, value):
        if isinstance(value, str) and len(value.strip()) == 0:
            raise ValueError("不能为空")
        return value