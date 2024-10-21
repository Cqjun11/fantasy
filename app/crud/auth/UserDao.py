from datetime import datetime

from app.models.user import User
from app.models import async_session
from sqlalchemy import update, select, or_
from app.middleware.Jwt import UserToken


class UserDao:
    # log = Log("UserDao")

    # async def updata_user(self, user_info, user_id: int):
    #     """编辑用户信息"""
    #     try:
    #         async with async_session() as session:
    #             async with session.begin():
    #                 querry = await session.execute(update(User).where(User.id == user_info.id)
    #     return await user.save()

    @staticmethod
    async def register_user(username: str, password: str):
        try:
            async with async_session() as session:
                async with session.begin():
                    existing_user = await session.execute(
                        select(User).where(User.username == username))
                    if existing_user.scalars().first():
                        raise Exception("用户名或邮箱已存在")
                    pwd = UserToken.add_salt(password)
                    user = User(username, pwd)
                    user.last_login_at = datetime.now()
                    session.add(user)
                    await session.commit()
            return user
        except Exception as e:
            # UserDao.log.error(f"用户注册失败: {str(e)}")
            raise Exception(f"注册失败: {e}")

    @staticmethod
    async def login(username, password):
        """校验登录"""
        try:
            pwd = UserToken.add_salt(password)
            async with async_session() as session:
                async with session.begin():
                    user = await session.execute(
                        select(User).where(User.username == username).where(User.password == pwd))
                    user = user.scalars().first()
                    if user is None:
                        raise Exception("用户名或密码错误")
                    user.last_login_at = datetime.now()
                    session.add(user)
                    await session.commit()
            return user
        except Exception as e:
            # UserDao.log.error(f"用户{username}登录失败: {str(e)}")
            raise e



