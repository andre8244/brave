import sys
import pygame

from pygame.locals import *
from robot.differential_drive_robot import DifferentialDriveRobot
from util.color import Color

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600

ROBOT_SIZE = 30
ROBOT_WHEEL_RADIUS = 10
ROBOT_WHEEL_SPEED_DELTA = 3

SCREEN_MARGIN = ROBOT_SIZE / 2

robot = None


def reset_scene():
    global robot

    robot = DifferentialDriveRobot(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, ROBOT_SIZE, ROBOT_WHEEL_RADIUS)


def print_wheels_speed():
    print('speed_left_wheel:', robot.speed_left_wheel, 'speed_right_wheel:', robot.speed_right_wheel)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Differential drive - BRAVE")
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    reset_scene()

    while True:
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[K_q]:
            robot.speed_left_wheel += ROBOT_WHEEL_SPEED_DELTA
            print_wheels_speed()
        elif keys_pressed[K_a]:
            robot.speed_left_wheel -= ROBOT_WHEEL_SPEED_DELTA
            print_wheels_speed()
        elif keys_pressed[K_w]:
            robot.speed_right_wheel += ROBOT_WHEEL_SPEED_DELTA
            print_wheels_speed()
        elif keys_pressed[K_s]:
            robot.speed_right_wheel -= ROBOT_WHEEL_SPEED_DELTA
            print_wheels_speed()
        elif keys_pressed[K_UP]:
            robot.speed_left_wheel += ROBOT_WHEEL_SPEED_DELTA
            robot.speed_right_wheel += ROBOT_WHEEL_SPEED_DELTA
            print_wheels_speed()
        elif keys_pressed[K_DOWN]:
            robot.speed_left_wheel -= ROBOT_WHEEL_SPEED_DELTA
            robot.speed_right_wheel -= ROBOT_WHEEL_SPEED_DELTA
            print_wheels_speed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_r:
                reset_scene()

        robot.step()

        # teletrasporto ai margini
        if robot.x < -SCREEN_MARGIN:
            robot.x = SCREEN_WIDTH + SCREEN_MARGIN
        if robot.x > SCREEN_WIDTH + SCREEN_MARGIN:
            robot.x = -SCREEN_MARGIN
        if robot.y < -SCREEN_MARGIN:
            robot.y = SCREEN_HEIGHT + SCREEN_MARGIN
        if robot.y > SCREEN_HEIGHT + SCREEN_MARGIN:
            robot.y = -SCREEN_MARGIN

        screen.fill(Color.BLACK)
        robot.draw(screen)

        pygame.display.flip()
        clock.tick(25)

