import pygame

from scene.obstacle import Obstacle
from color import Color


class Wall(Obstacle):

    def __init__(self, point1, point2, color):
        self.point1 = point1
        self.point2 = point2
        self.label = None

        vertices = [(point1.x, point1.y), (point2.x, point2.y)]
        edges = [[point1, point2]]
        super().__init__(vertices, edges, color)

    def get_saved_scene_repr(self):
        return self.__class__.__name__ + ' ' + str(self.point1.x) + ' ' + str(self.point1.y) \
               + ' ' + str(self.point2.x) + ' ' + str(self.point2.y)

    def set_label(self, label):
        self.label = label

    def draw_label(self, screen):
        if pygame.font:
            font = pygame.font.Font(None, 26)
            text = font.render(str(self.label), 1, Color.YELLOW, Color.DARK_GRAY)
            rect_x = (self.point1.x + self.point2.x) / 2
            rect_y = (self.point1.y + self.point2.y) / 2

            text_pos = pygame.Rect(rect_x, rect_y, 50, 50)
            screen.blit(text, text_pos)
