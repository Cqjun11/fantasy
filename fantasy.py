import uvicorn
from app import fantasy
from app.routers.auth import user
from app.routers.request import http
from app.routers.project import project
from config import BaseConfig
fantasy.include_router(user.router)
fantasy.include_router(http.router)
fantasy.include_router(project.router)

if __name__ == "__main__":
    # config = BaseConfig()
    # uvicorn.run('app:fantasy', host="127.0.0.1", port=8080, reload=False)
    # print(BaseConfig.SERVER_HOST, BaseConfig.SERVER_PORT)
    uvicorn.run("app:fantasy", host=BaseConfig.SERVER_HOST, port=BaseConfig.SERVER_PORT,
                log_level="debug", forwarded_allow_ips="*")
