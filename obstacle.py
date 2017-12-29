import pygame


class Obstacle:

    def __init__(self, vertices, edges, color):
        self.vertices = vertices
        self.edges = edges
        self.color = color

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.vertices, 1)
