import os.path
import sys
from pprint import pformat
from config import BaseConfig
from fastapi import FastAPI
from loguru import logger
from loguru._defaults import LOGURU_FORMAT
import logging
from app.models import create_tables

fantasy = FastAPI(debug=True)


@fantasy.on_event("startup")
async def startup():
    await create_tables()


# 配置日志格式
INFO_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> " \
              "| <level>{level: <8}</level> | <cyan>文件: {extra[filename]}</cyan> " \
              "| 模块: <cyan>{extra[business]}</cyan> | 方法: <cyan>{extra[func]}</cyan> " \
              "| <cyan>行数: {extra[line]}</cyan> | - <level>{message}</level>"

ERROR_FORMAT = "<red>{time:YYYY-MM-DD HH:mm:ss.SSS}</red> " \
               "| <level>{level: <8}</level> | <cyan>文件: {extra[filename]}</cyan> " \
               "| 模块: <cyan>{extra[business]}</cyan> | 方法: <cyan>{extra[func]}</cyan> " \
               "| <cyan>行数: {extra[line]}</cyan> | - <level>{message}</level>"


class InterceptHandler(logging.Handler):

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def format_record(record: dict) -> str:
    """
    这里的代码是copy的，记录日志格式的
    Custom format for loguru loggers.
    Uses pformat for log any data like request/response body during debug.
    Works with logging if loguru handler it.
    Example:
    # >>> payload = [{"users":[{"name": "Nick", "age": 87, "is_active": True}, {"name": "Alex", "age": 27, "is_active": True}], "count": 2}]
    # >>> logger.bind(payload=).debug("users payload")
    # >>> [   {   'count': 2,
    # >>>         'users': [   {'age': 87, 'is_active': True, 'name': 'Nick'},
    # >>>                      {'age': 27, 'is_active': True, 'name': 'Alex'}]}]
    """

    format_string = LOGURU_FORMAT
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


def make_filter(name):
    # 过滤操作，当日志要选择对应的日志文件的时候，通过filter进行筛选
    def filter_(record):
        return record["extra"].get("name") == name

    return filter_


def init_logging():
    loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("corn.")
    )
    for corn_logger in loggers:
        corn_logger.handlers = []

    intercept_handler = InterceptHandler()
    logging.getLogger("uvicorn").handlers = [intercept_handler]
    # 添加一个info log文件，主要记录debug和info级别的日志
    log_info = os.path.join(BaseConfig.log_str, "{}.log".format(BaseConfig.LOG_INFO))
    # 添加一个error log文件，主要记录warning和error级别的日志
    log_error = os.path.join(BaseConfig.log_str, "{}.log".format(BaseConfig.LOG_ERROR))
    logger.add(log_info, enqueue=True, rotation="20 Mb", level="DEBUG", filter=make_filter(BaseConfig.LOG_INFO))
    logger.add(log_error, enqueue=True, rotation="20 Mb", level="WARNING", filter=make_filter(BaseConfig.LOG_ERROR))

    # 配置loguru的日志句柄，sink代表输出的目标
    logger.configure(
        handlers=[
            {"sink": sys.stdout, "level": logging.DEBUG, "format": format_record},
            {"sink": log_info, "level": logging.INFO, "format": INFO_FORMAT,
             "filter": make_filter(BaseConfig.LOG_INFO)},
            {"sink": log_error, "level": logging.WARNING, "format": ERROR_FORMAT,
             "filter": make_filter(BaseConfig.LOG_ERROR)}
        ]
    )
    return logger


log = init_logging()

# log.bind(name='log_info').info("初始化日志配置")
