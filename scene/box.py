from point import Point
from scene.obstacle import Obstacle


class Box(Obstacle):

    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        vert1 = Point(x - size / 2, y - size / 2)
        vert2 = Point(x + size / 2, y - size / 2)
        vert3 = Point(x + size / 2, y + size / 2)
        vert4 = Point(x - size / 2, y + size / 2)

        vertices = [(vert1.x, vert1.y), (vert2.x, vert2.y), (vert3.x, vert3.y), (vert4.x, vert4.y)]
        edges = [[vert1, vert2], [vert2, vert3], [vert3, vert4], [vert4, vert1]]

        super().__init__(vertices, edges, color)

    def to_string(self):
        return self.__class__.__name__ + ' ' + str(self.x) + ' ' + str(self.y) + ' ' + str(self.size)

