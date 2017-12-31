import sys
import pygame
import math
import random

from pygame.locals import *
from robot.sensor_driven_robot import SensorDrivenRobot
from color import Color
from scene.scene import Scene
from scene.box import Box
from scene.wall import Wall
from sensor.proximity_sensor import ProximitySensor
from actuator import Actuator
from robot.motor_controller import MotorController
from point import Point


SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600

ROBOT_SIZE = 25

SCENE_SPEED_INITIAL = 2

scene = None
robots = None
obstacles = None


def init_scene(screen):
    global scene
    global robots
    global obstacles

    robots = []
    obstacles = []
    scene = Scene(SCENE_SPEED_INITIAL, screen)

    with open('saved_scene/scene.txt') as f:
        for line in f:
            words = line.split()

            if words[0] == 'Box':
                x = int(words[1])
                y = int(words[2])
                size = int(words[3])
                b = Box(x, y, size, Color.random_bright())
                scene.put(b)
    f.closed


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    init_scene(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_r:
                init_scene(screen)

        screen.fill(Color.BLACK)

        for obj in scene.objects:
            obj.draw(screen)

        pygame.display.flip()
        int_scene_speed = int(round(scene.speed))
        clock.tick(int_scene_speed)
