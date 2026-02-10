from cadbuildr.foundation import *

class Cube(Part):
    def __init__(self, size=20):
        self.size = size
        s = Sketch(self.xy())
        square = Square.from_center_and_side(s.origin, self.size)
        self.add_operation(Extrusion(square, self.size / 2, -self.size / 2))

if __name__ == '__main__':
    show(Cube())
