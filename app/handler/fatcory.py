from datetime import datetime
from app.handler.encoder import jsonable_encoder

class FantasyResponse:

    @staticmethod
    def model_to_dict(obj, *ignore: str):
        if getattr(obj, '__table__', None) is None:
            return obj
        data = dict()
        for c in obj.__table__.columns:
            if c.name in ignore:
                # 如果字段忽略, 则不进行转换
                continue
            val = getattr(obj, c.name)
            if isinstance(val, datetime):
                data[c.name] = val.strftime("%Y-%m-%d %H:%M:%S")
            else:
                data[c.name] = val
        return data

    @staticmethod
    def dict_model_to_dict(obj):
        for k, v in obj.items():
            if isinstance(v, dict):
                FantasyResponse.dict_model_to_dict(v)
            elif isinstance(v, list):
                obj[k] = FantasyResponse.model_to_list(v)
            else:
                obj[k] = FantasyResponse.model_to_dict(v)
        return obj

    @staticmethod
    def encode_json(data: dict, *exclude: str):
        return jsonable_encoder(data, exclude=exclude, custom_encoder={
            datetime: lambda x: x.strftime("%Y-%m-%d %H:%M:%S")
        })

    # @staticmethod
    # def jsonable_encoder():
    #

    @staticmethod
    def success(data=None, code=0, msg="操作成功", exclude=()):
        return FantasyResponse.encode_json(dict(code=code, msg=msg, data=data), *exclude)
        # return '登录成功'

    @staticmethod
    def model_to_list(data: list, *ignore: str):
        return [FantasyResponse.model_to_dict(x, *ignore) for x in data]

    @staticmethod
    def failed(msg, code=110, data=None):
        return dict(code=code, msg=str(msg), data=data)