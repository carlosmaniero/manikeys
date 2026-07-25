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
            "--stls", help="Comma-separated list of STL dependencies"
        )
        parser.add_argument(
            "--py-deps",
            help="Comma-separated list of Python dependencies",
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
            argv = [*argv, "--help"]

        args = parser.parse_args(argv[1:])

        dep_manager = self.dep_manager
        if args.stls and dep_manager is not None:
            dep_manager.resolve(args.stls)

        if args.output:
            self.save(args.output)
        elif args.show:
            self.show()

        if args.stls and dep_manager is not None:
            dep_manager.verify_all_used()

        expected_py_deps = set()
        if args.py_deps:
            expected_py_deps.update(
                d.strip() for d in args.py_deps.split(",") if d.strip()
            )

        from core.dependencies import (
            collect_python_dependencies,
            PROJECT_ROOT,
        )
        import sys
        from pathlib import Path

        actual_py_deps = collect_python_dependencies(self)
        try:
            own_file = str(
                Path(sys.argv[0]).resolve().relative_to(PROJECT_ROOT)
            )
            actual_py_deps.discard(own_file)
        except Exception:
            pass

        self._validate_unused_python_deps(expected_py_deps, actual_py_deps)
        self._validate_missing_python_deps(expected_py_deps, actual_py_deps)

    def _validate_unused_python_deps(
        self, expected: set[str], actual: set[str]
    ) -> None:
        unused = expected - actual
        if unused:
            raise RuntimeError(
                f"The following Python dependencies passed were not used by {self.__class__.__name__}: {sorted(list(unused))}"
            )

    def _validate_missing_python_deps(
        self, expected: set[str], actual: set[str]
    ) -> None:
        missing = actual - expected
        if missing:
            raise RuntimeError(
                f"The following Python dependencies were used by {self.__class__.__name__} but not declared in --py-deps: {sorted(list(missing))}"
            )
