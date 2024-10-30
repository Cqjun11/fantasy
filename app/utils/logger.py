import inspect
import os
from loguru import logger
from config import BaseConfig


class Log:
    business = None

    def __init__(self, name="fantasy"):
        """name 为业务名称"""
        if not os.path.exists(BaseConfig.log_str):
            os.makedirs(BaseConfig.log_str)
        self.business = name

    def info(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=BaseConfig.LOG_INFO, func=func, line=line,
                    business=self.business, filename=file_name).info(message)

    def error(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=BaseConfig.LOG_ERROR, func=func, line=line,
                    business=self.business, filename=file_name).error(message)

    def warning(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=BaseConfig.LOG_ERROR, func=func, line=line,
                    business=self.business, filename=file_name).warning(message)

    def debug(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=BaseConfig.LOG_INFO, func=func, line=line,
                    business=self.business, filename=file_name).debug(message)

    def exception(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=BaseConfig.LOG_ERROR, func=func, line=line,
                    business=self.business, filename=file_name).exception(message)


log = Log()
