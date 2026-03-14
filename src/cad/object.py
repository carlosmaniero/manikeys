from abc import ABC, abstractmethod
from typing import Protocol


class Saveable(Protocol):
    def save(self, path: str) -> None: ...


class Object(ABC):
    @abstractmethod
    def assemble(self) -> Saveable:
        pass

    def save(self):
        obj = self.assemble()
        obj.save(f"build/{self.__class__.__name__.lower()}.stl")
