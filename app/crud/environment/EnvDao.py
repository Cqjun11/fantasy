from datetime import datetime

from app.models import async_session
from app.models.environment import Environment
from sqlalchemy import update, select, or_


class EnvDao:

    @staticmethod
    async def add_env(name: str):
        try:
            async with async_session() as session:
                async with session.begin():
                    env = await session.execute(select(Environment).where(Environment.env_name == name))
                    if env is not None:
                        raise Exception("环境名称重复")
                    env = Environment(name)
                    env.created_at = datetime.now()
                    session.add(env)
                    # await session.commit()
                return env
        except Exception as e:
            raise Exception("添加失败")
