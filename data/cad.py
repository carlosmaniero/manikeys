from injector import Module, singleton
from cad.cap import CapCAD
from cad.keyboard import KeyboardCAD


class CADModule(Module):
    def configure(self, binder):
        binder.bind(CapCAD, scope=singleton)
        binder.bind(KeyboardCAD, scope=singleton)
