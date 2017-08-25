import sys
import pygame
from math import pi

from pygame.locals import *
from rot_triangle import RotTriangle
from color import Color

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600

ROBOT_SIZE = 50
ROBOT_INITIAL_SPEED = 10
ROBOT_INITIAL_DIRECTION = 0
ROBOT_DIRECTION_DELTA = pi / 16
ROBOT_SPEED_DELTA = 1

SCREEN_MARGIN = ROBOT_SIZE / 2

dd_robot = None


def reset_scene():
    global dd_robot

    dd_robot = RotTriangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, ROBOT_SIZE, Color.GREEN, Color.BLACK, ROBOT_INITIAL_DIRECTION)

def check_direction_limits():
    if dd_robot.direction > pi:
        dd_robot.direction -= 2 * pi
    elif dd_robot.direction < -pi:
        dd_robot.direction += 2 * pi

def turn_left():
    if dd_robot.speed >= 0:
        dd_robot.direction += ROBOT_DIRECTION_DELTA
    else:
        dd_robot.direction -= ROBOT_DIRECTION_DELTA
    check_direction_limits()


def turn_right():
    if dd_robot.speed >= 0:
        dd_robot.direction -= ROBOT_DIRECTION_DELTA
    else:
        dd_robot.direction += ROBOT_DIRECTION_DELTA
    check_direction_limits()


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    reset_scene()

    tick = 0

    while True:
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[K_LEFT]:
            turn_left()
        elif keys_pressed[K_RIGHT]:
            turn_right()
        elif keys_pressed[K_UP]:
            dd_robot.speed += ROBOT_SPEED_DELTA
        elif keys_pressed[K_DOWN]:
            dd_robot.speed -= ROBOT_SPEED_DELTA

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()

        dd_robot.move()

        tick += 1

        if tick % 25 == 0:
            print('robot dir:', dd_robot.direction)

        # teletrasporto ai margini
        if dd_robot.x < -SCREEN_MARGIN:
            dd_robot.x = SCREEN_WIDTH + SCREEN_MARGIN
        if dd_robot.x > SCREEN_WIDTH + SCREEN_MARGIN:
            dd_robot.x = -SCREEN_MARGIN
        if dd_robot.y < -SCREEN_MARGIN:
            dd_robot.y = SCREEN_HEIGHT + SCREEN_MARGIN
        if dd_robot.y > SCREEN_HEIGHT + SCREEN_MARGIN:
            dd_robot.y = -SCREEN_MARGIN

        screen.fill(Color.BLACK)
        dd_robot.draw(screen)

        pygame.display.flip()
        clock.tick(25)

