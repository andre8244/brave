import sys
import pygame

from pygame.locals import *
from differential_drive_robot import DifferentialDriveRobot
from color import Color

# TODO http://enesbot.me/kinematic-model-of-a-differential-drive-robot.html

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600

ROBOT_SIZE = 30
ROBOT_WHEEL_RADIUS = 10
ROBOT_WHEEL_SPEED_DELTA = 3

SCREEN_MARGIN = ROBOT_SIZE / 2

dd_robot = None


def reset_scene():
    global dd_robot

    dd_robot = DifferentialDriveRobot(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, ROBOT_SIZE, ROBOT_WHEEL_RADIUS)


def print_wheels_speed():
    print('speed_left_wheel:', dd_robot.speed_left_wheel, 'speed_right_wheel:', dd_robot.speed_right_wheel)


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    reset_scene()

    while True:
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[K_q]:
            dd_robot.speed_left_wheel += ROBOT_WHEEL_SPEED_DELTA
            print_wheels_speed()
        elif keys_pressed[K_a]:
            dd_robot.speed_left_wheel -= ROBOT_WHEEL_SPEED_DELTA
            print_wheels_speed()
        elif keys_pressed[K_w]:
            dd_robot.speed_right_wheel += ROBOT_WHEEL_SPEED_DELTA
            print_wheels_speed()
        elif keys_pressed[K_s]:
            dd_robot.speed_right_wheel -= ROBOT_WHEEL_SPEED_DELTA
            print_wheels_speed()
        elif keys_pressed[K_UP]:
            dd_robot.speed_left_wheel += ROBOT_WHEEL_SPEED_DELTA
            dd_robot.speed_right_wheel += ROBOT_WHEEL_SPEED_DELTA
            print_wheels_speed()
        elif keys_pressed[K_DOWN]:
            dd_robot.speed_left_wheel -= ROBOT_WHEEL_SPEED_DELTA
            dd_robot.speed_right_wheel -= ROBOT_WHEEL_SPEED_DELTA
            print_wheels_speed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_r:
                reset_scene()

        dd_robot.step()

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

