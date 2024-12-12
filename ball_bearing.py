from cadbuildr.foundation import *


class BallBearing626D(Part):
    # Key dimensions of the 626D ball bearing
    OUTER_DIAMETER = 19  # mm
    INNER_DIAMETER = 6  # mm
    HEIGHT = 6  # mm

    def __init__(self):
        # Create the outer cylinder
        self.create_outer_cylinder()
        # Cut the inner hole
        self.create_inner_hole()

    def create_outer_cylinder(self):
        # Sketch on the XY plane
        sketch = Sketch(self.xy())
        # Create a circle with the outer diameter
        outer_circle = Circle(center=sketch.origin, radius=self.OUTER_DIAMETER / 2)
        # Extrude the circle to create a cylinder
        extrusion = Extrusion(outer_circle, self.HEIGHT)
        self.add_operation(extrusion)

    def create_inner_hole(self):
        # Sketch on the XY plane
        sketch = Sketch(self.xy())
        # Create a circle with the inner diameter
        inner_circle = Circle(center=sketch.origin, radius=self.INNER_DIAMETER / 2)
        # Extrude the circle to remove material, creating the hole
        hole_extrusion = Extrusion(inner_circle, self.HEIGHT, cut=True)
        self.add_operation(hole_extrusion)
