from __future__ import annotations
import inspect
from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import Dict, List, Generic, TypeVar, Callable, Any, Set

PROJECT_ROOT = Path(__file__).resolve().parents[2]

T = TypeVar("T")


class DependencyManager(Generic[T]):
    def __init__(
        self,
        load_fn: Callable[[List[str]], List[T]],
        deps: List[str] | None = None,
    ):
        self._deps: List[str] = [d for d in (deps or []) if d.strip()]
        self._used: set[str] = set()
        self._load_fn = load_fn
        self._cache: Dict[str, T] = {}
        self.stls: MagicDependencyMap[T] | None = None

        if self._deps:
            loaded = self._load_fn(self._deps)
            for path, obj in zip(self._deps, loaded):
                self._cache[path] = obj
            self.resolve()

    def resolve(
        self, stls: str | List[str] | None = None
    ) -> MagicDependencyMap[T]:
        if stls:
            if isinstance(stls, str):
                deps_list = [d.strip() for d in stls.split(",") if d.strip()]
            else:
                deps_list = stls
            self._deps = deps_list
            if self._deps:
                loaded = self._load_fn(self._deps)
                for path, obj in zip(self._deps, loaded):
                    self._cache[path] = obj
        if not hasattr(self, "stls") or self.stls is None:
            self.stls = MagicDependencyMap(self)
        return self.stls

    def get(self, dep_path: str) -> T:
        if dep_path not in self._cache:
            raise KeyError(
                f"Dependency '{dep_path}' was requested but not provided in --stls list."
            )
        self._used.add(dep_path)
        return self._cache[dep_path]

    def verify_all_used(self) -> None:
        if not self._deps:
            return
        unused = set(self._deps) - self._used
        if unused:
            raise RuntimeError(
                f"The following dependencies passed in --deps were not used: {sorted(list(unused))}"
            )


class MagicDependencyMap(Generic[T]):
    def __init__(self, manager: DependencyManager[T]):
        self._manager = manager

    def __getitem__(self, key: str) -> T:
        return self._manager.get(key)

    def __contains__(self, key: object) -> bool:
        if isinstance(key, str):
            return key in self._manager._deps
        return False


def collect_python_dependencies(
    obj: Any, visited: Set[int] | None = None
) -> Set[str]:
    if visited is None:
        visited = set()

    obj_id = id(obj)
    if obj_id in visited:
        return set()
    visited.add(obj_id)

    deps: Set[str] = set()

    obj_type = type(obj)
    try:
        source_file = inspect.getfile(obj_type)
        rel_path = Path(source_file).resolve().relative_to(PROJECT_ROOT)
        if str(rel_path).startswith("src/"):
            deps.add(str(rel_path))
    except (TypeError, ValueError):
        pass

    if is_dataclass(obj):
        for f in fields(obj):
            val = getattr(obj, f.name, None)
            if val is not None:
                deps.update(collect_python_dependencies(val, visited))

    return deps
