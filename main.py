import argparse
from typing import List, Optional

from dependencyinjection.di_container import DIContainer
from parser.IArgParser import IArgParser

container = DIContainer.get_container()

def get_parser(args) -> Optional[IArgParser]:
    parsers = container[List[IArgParser]]
    for p in parsers:
        if p.get_component_name() == args.parser:
            return p
    return None


def main():
    parser = argparse.ArgumentParser(description="Parse data from .bin files.")
    subparsers = parser.add_subparsers(dest="parser", help="Specify the parsing type.")

    # First add all subparsers.
    for e in container[List[IArgParser]]:
        e.add_parser(subparsers)

    # Look for the asked component and then pass args.
    args = parser.parse_args()
    component_parser = get_parser(args)

    if component_parser is not None:
        component_parser.handle_parse(args, container)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()