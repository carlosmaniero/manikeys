from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Sequence
import argparse

T = TypeVar("T")


class Object(ABC, Generic[T]):
    @abstractmethod
    def assemble(self) -> T:
        pass

    @abstractmethod
    def save(self, path: str):
        pass

    @abstractmethod
    def show(self):
        pass

    def _get_program_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument("-o", "--output", help="Save the object to a file")
        parser.add_argument(
            "--show", action="store_true", help="Show the object"
        )
        return parser

    def program(self, argv: Sequence[str]):
        parser = self._get_program_parser()

        if len(argv) == 1:
            parser.print_help()
            exit(1)

        args = parser.parse_args(argv[1:])

        if args.output:
            self.save(args.output)

        if args.show:
            self.show()
