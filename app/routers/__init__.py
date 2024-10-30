from fastapi import Header
from starlette import status
from app.middleware.Jwt import UserToken
from app.exception.requests import AuthException, PermissionException
from app.crud.auth.UserDao import UserDao
from config import BaseConfig
from app.handler.fatcory import FantasyResponse
FORBIDDEN = "对不起, 你没有足够的权限"
class Permission:
    def __init__(self, role: int = BaseConfig.MEMBER):
        self.role = role

    async def __call__(self, token: str = Header(...)):
        if not token:
            raise AuthException(status.HTTP_200_OK, "用户信息身份认证失败, 请检查")
        try:
            user_info = UserToken.parse_token(token)
            if user_info.get("role", 0) < self.role:
                raise PermissionException(status.HTTP_200_OK, FORBIDDEN)
            user = await UserDao.query_user(user_info['id'])
            if user is None:
                raise Exception("用户不存在")
            user_info = FantasyResponse.model_to_dict(user, "password")
        except PermissionException as e:
            raise e
        except Exception as e:
            raise AuthException(status.HTTP_200_OK, str(e))
        return user_info

