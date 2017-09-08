import pygame

from rot_surface import RotSurface


class Box(RotSurface):
    def __init__(self, x, y, size, color_fg, color_bg, direction):
        self.size = size
        self.color_fg = color_fg
        self.color_bg = color_bg
        self.surf = pygame.Surface((size, size))
        self.surf.fill(color_fg)

        super().__init__(x, y, direction, self.surf)
