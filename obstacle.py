import pygame

from point import Point


class Obstacle:
    def __init__(self, x, y, size, color):
        vert1 = Point(x - size / 2, y - size / 2)
        vert2 = Point(x + size / 2, y - size / 2)
        vert3 = Point(x + size / 2, y + size / 2)
        vert4 = Point(x - size / 2, y + size / 2)

        self.vertices = [(vert1.x, vert1.y), (vert2.x, vert2.y), (vert3.x, vert3.y), (vert4.x, vert4.y)]
        self.edges = [[vert1, vert2], [vert2, vert3], [vert3, vert4], [vert4, vert1]]

        self.color = color
        # self.color_bg = color_bg
        # self.surf = pygame.Surface((size, size))
        # self.surf.fill(color_fg)

        # super().__init__(x, y, 0, self.surf)

    # TODO
    # def __init__(self, edge_list, color_fg):
    #     pass

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.vertices, 1)
