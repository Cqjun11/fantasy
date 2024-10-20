import uvicorn
from app import fantasy
from app.routers.auth import user
from config import BaseConfig
fantasy.include_router(user.router)

if __name__ == "__main__":
    # config = BaseConfig()
    # uvicorn.run('app:fantasy', host="127.0.0.1", port=8080, reload=False)
    # print(BaseConfig.SERVER_HOST, BaseConfig.SERVER_PORT)
    uvicorn.run("app:fantasy", host=BaseConfig.SERVER_HOST, port=BaseConfig.SERVER_PORT, reload=False, forwarded_allow_ips ="*")
