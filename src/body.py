from context import injector
from cad.body import BodyCAD
import openscad as osc

if __name__ == "__main__":
    body = injector.get(BodyCAD)
    body_cad = body.assembly()
    body_cad = osc.color(body_cad, "#333333")
    body_cad.show()
