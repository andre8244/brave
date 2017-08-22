import sys
import pygame
import math

from pygame.locals import *
from movingSquare import MovingSquare
from square import Square
from rotTriangle import RotTriangle

# creare modulo costanti colori

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
BLACK = 0, 0, 0
GREEN = 0, 255, 0
YELLOW = 255, 255, 0

robot_size = None
robot_speed = None
bat_size = None

def resetScene():
    global tri
    tri = RotTriangle(100, 100, 20, GREEN, BLACK, math.pi, 15)

    color = tri.surf.get_at((5, 10))
    print('color:', color)

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    resetScene()

    while True:
        # keys_pressed = pygame.key.get_pressed()
        #
        # if keys_pressed[K_DOWN]:
        #     robot.direction -= math.pi / 32
        # elif keys_pressed[K_UP]:
        #     robot.direction += math.pi / 32

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()

        screen.fill(BLACK)
        tri.draw(screen)

        pygame.display.flip()
        clock.tick(30)

