import pygame

from geometry.rot_surface import RotSurface
from util.color import Color


class Light(RotSurface):

    def __init__(self, x, y, emitting_power, color_fg, color_bg):
        self.emitting_power = emitting_power
        self.color_fg = color_fg
        self.color_bg = color_bg
        self.size = emitting_power
        self.label = None

        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(color_bg)
        self.surf.set_colorkey(color_bg)

        pygame.draw.circle(self.surf, color_fg, [int(round(self.size / 2)), int(round(self.size / 2))],
                           int(round(self.size / 2)))

        super().__init__(x, y, 0, self.surf)

    def get_saved_scene_repr(self):
        return self.__class__.__name__ + ' ' + str(self.x) + ' ' + str(self.y) + ' ' + str(self.emitting_power)

    def draw_label(self, screen):
        if pygame.font and self.label is not None:
            font = pygame.font.Font(None, 24)
            text = font.render(str(self.label), 1, Color.YELLOW, Color.DARK_GRAY)
            text_pos = pygame.Rect(self.x + (self.size / 2), self.y + (self.size / 2), 50, 50)
            screen.blit(text, text_pos)
