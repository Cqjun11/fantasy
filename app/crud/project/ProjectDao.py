import asyncio
from datetime import datetime
from typing import List

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
            roles = await session.execute(
                select(ProjectRole.project_id).where(ProjectRole.user_id == user, ProjectRole.deleted_at == 0))
            for role in roles.all():
                ans.add(role[0])
            roles = await session.execute(select(Project.id).where(Project.owner == user, Project.deleted_at == 0))
            for r in roles.all():
                ans.add(r[0])
            return list(ans) if len(ans) > 0 else None

    @classmethod
    async def add_project(cls, project_name, owner, user_id, project_description):
        """添加项目"""
        try:
            async with async_session() as session:
                async with session.begin():
                    data = await session.execute(
                        select(Project).where(Project.project_name == project_name, Project.deleted_at == 0))
                    if data.scalars().first() is not None:
                        raise Exception("项目已存在")
                    data = Project(project_name=project_name, owner=owner, create_user=user_id,
                                   project_describe=project_description)
                    session.add(data)
        except Exception as e:
            raise Exception("项目添加失败")

    @classmethod
    async def update_project(cls, id: int, project_name: str, owner: int, user_id: int, project_description: str,
                             role: int):
        """
        编辑项目信息
        id:
        project_name:
        owner:
        user_id:
        project_description:
        role:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    query = await session.execute(select(Project).where(Project.id == id, Project.deleted_at == 0))
                    data = query.scalars().first()
                    if data is None:
                        raise Exception("项目不存在")
                    if data.owner != owner and role < BaseConfig.ADMIN and data.owner != user_id:
                        raise Exception("没有权限修改项目")
                    data.project_name = project_name
                    data.project_describe = project_description
                    data.update_time = datetime.now()
                    data.update_user = user_id
        except Exception as e:
            raise Exception("编辑项目{}失败".format(project_name))

    @classmethod
    async def query_project(cls, id: int) -> (list[Project], list[ProjectRole]):
        """
        根据项目id查询项目与项目角色
        id
        Returns: 项目信息与项目角色
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    query = await session.execute(select(Project).where(Project.id == id, Project.deleted_at == 0))
                    data = query.scalars().first()
                    if data is None:
                        raise Exception("项目不存在")
                    roles = await ProjectRoleDao.list_role(id)
                    return data, roles
        except Exception as e:
            raise Exception("查询项目{}失败".format(id))

    # @classmethod
    # async def delete_project(cls, id: int, user_id: int, owner: int) -> None:
    #     """根据项目id删除项目"""



async def main():
    project = ProjectDao()
    await project.add_project("测试项目", 1, 1, "测试项目描述")


if __name__ == "__main__":
    asyncio.run(main())
