import inspect
import logging
from dataclasses import dataclass

from logger.ILogger import ILogger

class Logger(ILogger):
    __logger = logging.getLogger(__name__)

    @dataclass
    class LogContext:
        class_name: str
        method_name: str

    def __get_context(self):
        """Returns the name of the method and the class that were called up two times before this method call."""
        stack = inspect.stack()
        return self.LogContext(
            class_name=stack[2][0].f_locals["self"].__class__.__name__,
            method_name=stack[2][0].f_code.co_name
        )

    def info(self, msg, *args):
        if not msg: raise ValueError
        context = self.__get_context()
        self.__logger.info("{}.{}(): {}".format(context.class_name, context.method_name, msg), *args)

    def debug(self, msg, *args):
        if not msg: raise ValueError
        context = self.__get_context()
        self.__logger.debug("{}.{}(): {}".format(context.class_name, context.method_name, msg), *args)

    def critical(self, msg, *args):
        if not msg: raise ValueError
        context = self.__get_context()
        self.__logger.critical("{}.{}(): {}".format(context.class_name, context.method_name, msg), *args)

    def warning(self, msg, *args):
        if not msg: raise ValueError
        context = self.__get_context()
        self.__logger.warning("{}.{}(): {}".format(context.class_name, context.method_name, msg), *args)

    def error(self, msg, *args):
        if not msg: raise ValueError
        context = self.__get_context()
        self.__logger.error("{}.{}(): {}".format(context.class_name, context.method_name, msg), *args)
