import pygame

from geometry.rot_surface import RotSurface


class RotTriangle(RotSurface):

    def __init__(self, x, y, size, color_fg, color_bg, direction):
        self.size = size
        self.color_fg = color_fg
        self.color_bg = color_bg
        self.surf = pygame.Surface((size, size))
        self.surf.fill(color_bg)
        self.surf.set_colorkey(color_bg)

        # vertices with direction 0
        x1 = 0
        y1 = size / 4
        x2 = 0
        y2 = 0.75 * size
        x3 = size
        y3 = size / 2

        v1 = [x1, y1]
        v2 = [x2, y2]
        v3 = [x3, y3]

        pygame.draw.polygon(self.surf, self.color_fg, [v1, v2, v3])

        super().__init__(x, y, direction, self.surf)
