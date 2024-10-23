import hashlib
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError
import jwt

EXPIRED_HOUR = 72


class UserToken(object):
    key = 'fantasyToken'
    salt = 'fantasy'

    @staticmethod
    def get_token(data):
        """生成token
        :return : 过期时间 , token
        """
        expire = datetime.now(timezone.utc) + timedelta(hours=EXPIRED_HOUR)
        new_time = dict({"exp": expire}, **data)
        return expire.timestamp(), jwt.encode(new_time, key=UserToken.key)

    @staticmethod
    def parse_token(token):
        """token解密"""
        try:
            return jwt.decode(token, key=UserToken.key, algorithms=["HS256"])
        except ExpiredSignatureError:
            raise Exception("登录状态已过期, 请重新登录")
        except Exception:
            raise Exception("登录状态校验失败, 请重新登录")

    @staticmethod
    def add_salt(password):
        """密码MD5加密
        :return 加密后的密码
        """
        m = hashlib.md5()
        bt = f"{password}{UserToken.salt}".encode("utf-8")
        m.update(bt)
        return m.hexdigest()

#
# time, token = UserToken.get_token({"username": "admin", "password": "123456"})
# UserToken.parse_token(token)
# print(datetime.fromtimestamp(time))
# print(UserToken.add_salt('123456'))
# print(time, token)
