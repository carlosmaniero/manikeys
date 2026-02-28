from context import injector
from cad.keyboard import KeyboardCAD


fn = 200

if __name__ == "__main__":
    injector.get(KeyboardCAD).assembly().show()
