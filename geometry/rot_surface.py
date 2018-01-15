import math
import pygame


class RotSurface:

    def __init__(self, x, y, direction, surf):
        self.x = x
        self.y = y
        self.direction = direction
        self.surf = surf
        self.speed = 0

    def move(self):
        dx = self.speed * math.cos(self.direction)
        dy = self.speed * math.sin(self.direction)
        self.x += dx
        self.y += dy

    def draw(self, screen):
        degrees = math.degrees(self.direction)
        rotated_surf = pygame.transform.rotate(self.surf, degrees)
        rot_rect = rotated_surf.get_rect()
        rot_rect.center = (self.x, self.y)
        screen.blit(rotated_surf, rot_rect)
