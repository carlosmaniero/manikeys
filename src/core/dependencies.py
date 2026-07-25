from __future__ import annotations
from typing import Dict, List, Generic, TypeVar, Callable

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

    def resolve(self) -> MagicDependencyMap[T]:
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
