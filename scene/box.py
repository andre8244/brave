import pygame

from geometry.point import Point
from scene.obstacle import Obstacle
from util.color import Color


class Box(Obstacle):

    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.label = None

        vert1 = Point(x - size / 2, y - size / 2)
        vert2 = Point(x + size / 2, y - size / 2)
        vert3 = Point(x + size / 2, y + size / 2)
        vert4 = Point(x - size / 2, y + size / 2)

        vertices = [(vert1.x, vert1.y), (vert2.x, vert2.y), (vert3.x, vert3.y), (vert4.x, vert4.y)]
        edges = [[vert1, vert2], [vert2, vert3], [vert3, vert4], [vert4, vert1]]
        super().__init__(vertices, edges, color)

    def get_saved_scene_repr(self):
        return self.__class__.__name__ + ' ' + str(self.x) + ' ' + str(self.y) + ' ' + str(self.size)

    def draw_label(self, screen):
        if pygame.font:
            font = pygame.font.Font(None, 24)
            text = font.render(str(self.label), 1, Color.YELLOW, Color.DARK_GRAY)
            text_pos = pygame.Rect(self.x + (self.size / 2), self.y + (self.size / 2), 50, 50)
            screen.blit(text, text_pos)
