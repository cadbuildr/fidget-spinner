# %%
from foundation import *
import math

# Constants
OUTER_DIAMETER = 19
INNER_DIAMETER = 6
WIDTH = 6
SIDE_LENGTH = 100
CORNER_RADIUS = 20
BEARING_TOLERANCE = 0.4
BEARING_RADIUS = OUTER_DIAMETER / 2 + BEARING_TOLERANCE  # Radius for bearing holes
HOLE_RADIUS_DISTANCE = 30  # Distance from the center to the hole radius


class SimplifiedBearing(Part):
    def __init__(self):
        self.create_outer_body()
        self.cut_inner_body()
        self.paint("grey")

    def create_outer_body(self):
        sketch = Sketch(self.xy())
        outer_circle = Circle(sketch.origin, OUTER_DIAMETER / 2)
        extrusion = Extrusion(outer_circle, WIDTH)
        self.add_operation(extrusion)

    def cut_inner_body(self):
        sketch = Sketch(self.xy())
        inner_circle = Circle(sketch.origin, INNER_DIAMETER / 2)
        cut_extrusion = Extrusion(inner_circle, WIDTH, cut=True)
        self.add_operation(cut_extrusion)


class RoundedTriangleWithHoles(Part):
    def __init__(self):
        self.create_rounded_triangle()
        self.add_holes()
        self.paint("red")

    def create_rounded_triangle(self):
        sketch = Sketch(self.xy())
        p1 = Point(sketch, -SIDE_LENGTH / 2, -SIDE_LENGTH / (2 * (3**0.5)))
        p2 = Point(sketch, SIDE_LENGTH / 2, -SIDE_LENGTH / (2 * (3**0.5)))
        p3 = Point(sketch, 0, SIDE_LENGTH / (3**0.5))
        triangle = RoundedCornerPolygon(
            [Line(p1, p2), Line(p2, p3), Line(p3, p1)], CORNER_RADIUS
        )
        extrusion = Extrusion(triangle, WIDTH)
        self.add_operation(extrusion)

    def add_holes(self):
        sketch = Sketch(self.xy())
        center = Point(sketch, 0, 0)
        center_hole = Hole(center, BEARING_RADIUS, WIDTH)
        self.add_operation(center_hole)

        angular_offset = math.radians(90)
        for i in range(3):
            angle = angular_offset + math.radians(120 * i)
            x = HOLE_RADIUS_DISTANCE * math.cos(angle)
            y = HOLE_RADIUS_DISTANCE * math.sin(angle)
            hole_position = Point(sketch, x, y)
            hole = Hole(hole_position, BEARING_RADIUS, WIDTH)
            self.add_operation(hole)


class StructuralAssembly(Assembly):
    def __init__(self):
        self.create_assembly()

    def create_assembly(self):
        # Add the structural part
        structural_part = RoundedTriangleWithHoles()
        self.add_component(structural_part)

        # Add 4 independent bearings
        # Center bearing
        center_bearing = SimplifiedBearing()
        center_bearing_tf = TFHelper()
        self.add_component(center_bearing, center_bearing_tf.get_tf())

        # Outer bearings at 120-degree intervals
        angular_offset = math.radians(90)
        for i in range(3):
            angle = angular_offset + math.radians(120 * i)
            x = HOLE_RADIUS_DISTANCE * math.cos(angle)
            y = HOLE_RADIUS_DISTANCE * math.sin(angle)

            outer_bearing = SimplifiedBearing()  # Create a new bearing instance
            bearing_tf = TFHelper()
            bearing_tf.translate([x, y, 0])  # Translate to position
            self.add_component(outer_bearing, bearing_tf.get_tf())


# Display the assembly
show(StructuralAssembly())
# %%
