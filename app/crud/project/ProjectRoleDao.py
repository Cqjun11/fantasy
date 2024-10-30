from app.models import async_session
from sqlalchemy import Select, select
from app.models.project_role import ProjectRole
from app.models.project import Project


class ProjectRoleDao:

    @classmethod
    async def list_project_by_user(cls, user_id: int) -> list[int]:
        """通过userid获取项目列表"""
        try:
            async with async_session() as session:
                data = await session.execute(
                    Select(ProjectRole.project_id).where(ProjectRole.user_id == user_id, ProjectRole.deleted_at == 0)
                )
                return data.scalars().all()
        except Exception as e:
            raise Exception("获取项目列表失败", e)

    @staticmethod
    async def list_role(project_id: int) -> list[ProjectRole]:
        try:
            async with async_session() as session:
                query = await session.execute(
                    select(ProjectRole).where(ProjectRole.project_id == project_id, ProjectRole.deleted_at == 0))
                return query.scalars().all()
        except Exception as e:
            raise Exception(f"获取项目角色列表失败")


