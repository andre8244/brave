import pygame
from rot_surface import RotSurface


class Light(RotSurface):

    def __init__(self, x, y, emitting_power, color_fg, color_bg):
        self.emitting_power = emitting_power
        self.color_fg = color_fg
        self.color_bg = color_bg
        self.size = emitting_power

        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(color_bg)
        self.surf.set_colorkey(color_bg)

        pygame.draw.circle(self.surf, color_fg, [int(round(self.size / 2)), int(round(self.size / 2))],
                           int(round(self.size / 2)))

        super().__init__(x, y, 0, self.surf)
