from pydantic import BaseModel, field_validator


class ProjectForm(BaseModel):
    project_name: str
    owner: int
    project_description: str

    @field_validator('project_name', 'owner')
    def name_not_empty(cls, value):
        if isinstance(value, str) and len(value.strip()) == 0:
            raise ValueError("不能为空")
        return value


class ProjectRoleForm(BaseModel):
    user_id: int
    project_role: int
    project_id: int

    @field_validator('user_id', 'project_role', 'project_id')
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ValueError("不能为空")
        return v
