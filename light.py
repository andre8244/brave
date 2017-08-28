import pygame
from rot_surface import RotSurface

class Light(RotSurface):

    def __init__(self, x, y, size, color_fg, color_bg, emittingPower):
        self.size = size
        self.color_fg = color_fg
        self.color_bg = color_bg
        self.emittingPower = emittingPower

        self.surf = pygame.Surface((size, size))
        self.surf.fill(color_bg)
        self.surf.set_colorkey(color_bg)

        pygame.draw.circle(self.surf, color_fg, [int(round(size / 2)), int(round(size / 2))], int(round(size / 2)))

        super().__init__(x, y, 0, self.surf)
