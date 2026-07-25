from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Sequence, Iterator
import argparse

T = TypeVar("T")


class Object(ABC, Generic[T]):
    @abstractmethod
    def assemble(self) -> T | Iterator[T]:
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
        parser.add_argument(
            "--stls", help="Comma-separated list of dependencies"
        )
        return parser

    @property
    def deps(self):
        if not hasattr(self, "_dep_manager") or self._dep_manager is None:
            from core.dependencies import DependencyManager

            load_fn = getattr(self, "load_deps_fn", None)
            if load_fn is None:
                raise RuntimeError(
                    f"{self.__class__.__name__} does not define load_deps_fn to resolve dependencies"
                )
            self._dep_manager = DependencyManager(load_fn=load_fn)
        return self._dep_manager

    @property
    def dep_manager(self):
        if not hasattr(self, "_dep_manager"):
            from core.dependencies import DependencyManager

            load_fn = getattr(self, "load_deps_fn", None)
            if load_fn is None:
                return None
            self._dep_manager = DependencyManager(load_fn=load_fn)
        return self._dep_manager

    @dep_manager.setter
    def dep_manager(self, value):
        self._dep_manager = value

    def program(self, argv: Sequence[str]):
        parser = self._get_program_parser()

        if len(argv) == 1:
            parser.print_help()
            exit(1)

        args = parser.parse_args(argv[1:])

        deps_list = (
            [d.strip() for d in args.stls.split(",")] if args.stls else []
        )
        dep_manager = self.dep_manager
        if dep_manager is not None and deps_list:
            load_fn = getattr(
                dep_manager, "_load_fn", getattr(self, "load_deps_fn", None)
            )
            dep_manager.__init__(load_fn=load_fn, deps=deps_list)

        if args.output:
            self.save(args.output)

        if args.show:
            self.show()

        if args.stls and dep_manager is not None:
            dep_manager.verify_all_used()
