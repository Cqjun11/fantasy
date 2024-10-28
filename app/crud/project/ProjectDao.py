from sqlalchemy import or_, select, desc
from app.models.project import Project
from app.models.project_role import ProjectRole
from app.models import async_session
from config import BaseConfig
from app.crud.project.ProjectRoleDao import ProjectRoleDao


class ProjectDao:

    @classmethod
    async def list_project(cls, user_id: int, role: int, page: int, size: int, name: str = None) -> (
            list[Project], int):
        """
        查询/获取项目列表
        :param user_id: 当前用户
        :param role: 当前用户角色
        :param page: 当前页码
        :param size: 当前size
        :param name: 项目名称
        :return: 项目列表和总数
        """
        try:
            # search 为查找条件
            search = [Project.deleted_at == 0]
            async with async_session() as session:
                # 如果权限不是管理员
                if role != BaseConfig.ADMIN:
                    project_list = await ProjectRoleDao.list_project_by_user(user_id)
                    # 找出用户能看到的项目
                    search.append(or_(Project.id.in_(project_list), Project.owner == user_id))
                if name:
                    # 查找全部符合条件项目
                    search.append(Project.name.like("%{}%".format(name)))
                sql = select(Project).where(*search).order_by(desc(Project.update_time))
                data = await session.exec(sql)
                sql = sql.offset((page - 1) * size).limit(size)
                total = data.raw.rowcount
                data = await session.execute(sql)
                return data.scalars().all(), total
        except Exception as e:
            raise Exception(f"获取用户: {user_id}项目列表失败", e)

    @classmethod
    async def list_project_id_by_user(cls, user, role):
        """获取用户可见项目"""
        if role == BaseConfig.ADMIN:
            return []
        ans = set()
        async with async_session() as session:
            # 查询符合条件项目id
            roles = await session.execute(select(ProjectRole.project_id).where(ProjectRole.user_id ==user, ProjectRole.deleted_at==0))
            for role in roles.all():
                ans.add(role[0])
            roles = await session.execute(select(Project.id).where(Project.owner == user, Project.deleted_at == 0))
            for r in roles.all():
                ans.add(r[0])
            return list(ans) if len(ans) > 0 else None
