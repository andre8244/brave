import sys
import pygame
import math

from pygame.locals import *
from movingSquare import MovingSquare
from square import Square

# creare modulo costanti colori

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
BLACK = 0, 0, 0
GREEN = 0, 255, 0
YELLOW = 255, 255, 0

robot_size = None
robot_speed = None
bat_size = None

def resetScene():
    global robot
    global robot_size
    global robot_speed
    global robot_direction
    global light

    robot_size = 20
    robot_speed = 10
    robot_direction = -math.pi / 4

    robot = MovingSquare(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, robot_size, GREEN, robot_direction, robot_speed)

    light = Square(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4, 10, YELLOW)

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    resetScene()

    while True:
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[K_DOWN]:
            robot.direction -= math.pi / 32
        elif keys_pressed[K_UP]:
            robot.direction += math.pi / 32

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()

        robot = robot.move()

        screen.fill(BLACK)
        robot.draw(screen)
        light.draw(screen)

        pygame.display.flip()
        clock.tick(30)

