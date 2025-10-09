from abc import ABC, abstractmethod

from lagom import Container


class IArgParser(ABC):
    @abstractmethod
    def get_component_name(self) -> str:
        """Returns the component name used as the first argument in our application."""
        pass

    @abstractmethod
    def add_parser(self, subparser_root):
        """Adds all parsing arguments using argparse."""
        pass

    @abstractmethod
    def handle_parse(self, args, container: Container):
        """This is the code that will be executed if a user uses this component."""
        pass