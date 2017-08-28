import sys
import pygame
import math

from pygame.locals import *
from sensor_driven_robot import SensorDrivenRobot
from color import Color
from scene import Scene
from light import Light
from light_sensor import LightSensor
from actuator import Actuator
from motor_controller import MotorController

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600

ROBOT_SIZE = 30
ROBOT_WHEEL_RADIUS = 10
ROBOT_WHEEL_SPEED_DELTA = 3

LIGHT_SENSOR_DIRECTION = math.pi / 4
LIGHT_SENSOR_SATURATION_VALUE = 100

MOTOR_CONTROLLER_COEFFICIENT = 20
MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE = 15

SCREEN_MARGIN = ROBOT_SIZE / 2

scene = None
robot = None


def init_scene():
    global scene
    global robot

    scene = Scene()
    light = Light(600, 200, 20, Color.YELLOW, Color.BLACK, 50)
    light2 = Light(700, 250, 20, Color.YELLOW, Color.BLACK, 50)

    robot = SensorDrivenRobot(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, ROBOT_SIZE, ROBOT_WHEEL_RADIUS)

    left_light_sensor = LightSensor(robot, LIGHT_SENSOR_DIRECTION, LIGHT_SENSOR_SATURATION_VALUE, scene)
    right_light_sensor = LightSensor(robot, -LIGHT_SENSOR_DIRECTION, LIGHT_SENSOR_SATURATION_VALUE, scene)
    left_wheel_actuator = Actuator()
    right_wheel_actuator = Actuator()
    left_motor_controller = MotorController(right_light_sensor, MOTOR_CONTROLLER_COEFFICIENT, left_wheel_actuator, MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE)
    right_motor_controller = MotorController(left_light_sensor, MOTOR_CONTROLLER_COEFFICIENT, right_wheel_actuator, MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE)

    robot.set_left_motor_controller(left_motor_controller)
    robot.set_right_motor_controller(right_motor_controller)

    scene.put(robot)
    scene.put(light)
    scene.put(light2)


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    init_scene()

    tick = 0

    while True:
        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_r:
                init_scene()

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

        robot.sense_and_act()

        for obj in scene.objects:
            obj.draw(screen)

        pygame.display.flip()
        clock.tick(25)

