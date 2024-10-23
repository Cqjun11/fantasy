from fastapi import APIRouter
from app.crud.auth.UserDao import UserDao
from app.middleware.Jwt import UserToken
from app.handler.fatcory import FantasyResponse
from app.schema.user import UserDto


router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(data: UserDto):
    try:
        user = await UserDao.login(data.username, data.password)
        user = FantasyResponse.model_to_dict(user, "password")
        end_time, token = UserToken.get_token(user)
        return FantasyResponse.success(dict(token=token, user=user, end_time=end_time), msg="登录成功")
    except Exception as e:
        return FantasyResponse.failed(e)


@router.post("/register")
async def register(data: UserDto):
    try:
        user = await UserDao.register_user(data.username, data.password)
        user = FantasyResponse.model_to_dict(user, "password")
        end_time, token = UserToken.get_token(user)
        return FantasyResponse.success(dict(token=token, user=user, end_time=end_time), msg="注册成功")
    except Exception as e:
        return FantasyResponse.failed(e)

