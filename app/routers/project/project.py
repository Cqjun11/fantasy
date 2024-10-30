from fastapi import APIRouter, Depends
from app.handler.fatcory import FantasyResponse
from app.crud.project.ProjectDao import ProjectDao
from app.models.project_role import ProjectRole
from app.routers import Permission
from app.schema.project import ProjectForm, ProjectRoleForm

router = APIRouter(prefix="/project")


@router.get("/list")
async def list_projects(page: int = 1, size: int = 8, project_name: str = "", user_info=Depends(Permission())):
    user_role, user_id = user_info["role"], user_info["id"]
    result, total = await ProjectDao.list_project(user_id, user_role, page, size, project_name)
    return FantasyResponse.success_with_size(data=result, total=total)


@router.post("/create")
async def create_project(data: ProjectForm, user_info=Depends(Permission())):
    try:
        await ProjectDao.add_project(user_id=user_info["id"], **data.dict())
        return FantasyResponse.success()
    except Exception as e:
        return FantasyResponse.failed(e)


@router.post("/role/create")
async def create_project_role(role: ProjectRoleForm, user_info=Depends(Permission())):
    try:
