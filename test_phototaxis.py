import sys
import pygame

from pygame.locals import *
from differential_drive_robot import DifferentialDriveRobot
from color import Color
from sensor import Sensor
from square import Square
from math import atan2, cos, sin, pi


SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600

ROBOT_SIZE = 30
ROBOT_WHEEL_RADIUS = 10
ROBOT_WHEEL_SPEED_DELTA = 3

SCREEN_MARGIN = ROBOT_SIZE / 2

dd_robot = None
light = None
sensor = None


def reset_scene():
    global dd_robot
    global sensor
    global light

    dd_robot = DifferentialDriveRobot(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, ROBOT_SIZE, ROBOT_WHEEL_RADIUS)


    # sensor_surf = pygame.Surface((5, 5))
    # sensor_surf.fill(Color.YELLOW)
    #
    # sensor = Sensor(dd_robot.x + 40, dd_robot.y, dd_robot.direction, sensor_surf, 1)

    light = Square(400, 30, 5, Color.YELLOW)

def print_wheels_speed():
    print('speed_left_wheel:', dd_robot.speed_left_wheel, 'speed_right_wheel:', dd_robot.speed_right_wheel)


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    reset_scene()

    tick = 0

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


        # cambio SDR
        x_robot = dd_robot.x
        y_robot = -dd_robot.y
        x_light = light.x
        y_light = -light.y

        x_light -= x_robot
        y_light -= y_robot

        dir_light = atan2(y_light, x_light)
        dir_robot = dd_robot.direction
        difference_dir = dir_robot - dir_light

        angle_robot_light = atan2(sin(difference_dir), cos(difference_dir))


        tick +=1

        if tick % 20 == 0:
            print('===')
            print('x_light:', x_light, 'y_light:', y_light, 'dir_light:', dir_light)
            print('robot dir:', dd_robot.direction, 'angle_robot_light:', angle_robot_light)
            print('===')





        screen.fill(Color.BLACK)
        dd_robot.draw(screen)
        # sensor.draw(screen)
        light.draw(screen)

        pygame.display.flip()
        clock.tick(20)

