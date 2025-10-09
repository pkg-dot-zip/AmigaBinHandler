import argparse
from typing import List, Optional

from logger.ILogger import ILogger
from parser.IArgParser import IArgParser


class MainApp:
    def __init__(self, logger: ILogger, parsers: List[IArgParser]):
        self.logger = logger
        self.parsers = parsers

    def get_parser(self, args) -> Optional[IArgParser]:
        for p in self.parsers:
            if p.get_component_name() == args.parser:
                return p
        return None

    def main(self):
        parser = argparse.ArgumentParser(description="Parse data from .bin files.")
        subparsers = parser.add_subparsers(dest="parser", help="Specify the parsing type.")

        # First add all subparsers.
        for e in self.parsers:
            self.logger.info(f"Registering parser for '{e.get_component_name()}'")
            e.add_parser(subparsers)

        # Look for the asked component and then pass args.
        args = parser.parse_args()
        component_parser = self.get_parser(args)

        if component_parser is not None:
            component_parser.handle_parse(args)
        else:
            parser.print_help()