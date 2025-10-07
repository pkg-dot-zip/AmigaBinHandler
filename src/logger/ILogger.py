from abc import ABC, abstractmethod

class ILogger(ABC):

    @abstractmethod
    def info(self, msg, *args):
        """
        Logs a specified message at INFO level.
        :param msg: The message to log. Can not be empty.
        :param args: Ignore.
        """
        pass

    @abstractmethod
    def debug(self, msg, *args):
        """
        Logs a specified message at DEBUG level.
        :param msg: The message to log. Can not be empty.
        :param args: Ignore.
        """
        pass

    @abstractmethod
    def critical(self, msg, *args):
        """
        Logs a specified message at CRITICAL level.
        :param msg: The message to log. Can not be empty.
        :param args: Ignore.
        """
        pass

    @abstractmethod
    def warning(self, msg, *args):
        """
        Logs a specified message at WARNING level.
        :param msg: The message to log. Can not be empty.
        :param args: Ignore.
        """
        pass

    @abstractmethod
    def error(self, msg, *args):
        """
        Logs a specified message at ERROR level.
        :param msg: The message to log. Can not be empty.
        :param args: Ignore.
        """
        pass
