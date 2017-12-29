from obstacle import Obstacle


class Wall(Obstacle):

    def __init__(self, point1, point2, color):
        # vert1 = Point(x - size / 2, y - size / 2)
        # vert2 = Point(x + size / 2, y - size / 2)
        # vert3 = Point(x + size / 2, y + size / 2)
        # vert4 = Point(x - size / 2, y + size / 2)

        vertices = [(point1.x, point1.y), (point2.x, point2.y)]
        edges = [[point1, point2]]

        super().__init__(vertices, edges, color)
