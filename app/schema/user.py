from pydantic import BaseModel, field_validator


class UserDto(BaseModel):
    password: str
    username: str

    @field_validator("username", "password")
    def field_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ValueError("参数不能为空")
        return v
