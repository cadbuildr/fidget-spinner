def cube_vertices(side):
    s = side / 2.0
    return [
        (-s, -s, -s),
        (s, -s, -s),
        (s, s, -s),
        (-s, s, -s),
        (-s, -s, s),
        (s, -s, s),
        (s, s, s),
        (-s, s, s),
    ]

v = cube_vertices(10.0)
print("cube_vertices_count", len(v))
