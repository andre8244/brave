import sys
import pygame
import random

from pygame.locals import *
from color import Color
from scene.scene import Scene
from scene.box import Box
from scene.wall import Wall
from point import Point
from robot.sensor_driven_robot import SensorDrivenRobot


ROBOT_SIZE = 25
ROBOT_WHEEL_RADIUS = 10

SCENE_SPEED_INITIAL = 25

screen = None
scene = None
boxes_added = None
label = None


def init_scene():
    global screen
    global scene
    global boxes_added
    global label

    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = 'saved_scenes/scene.txt'

    with open(file_name) as f:
        line_number = 1

        for line in f:
            words = line.split()

            if words[0] == 'Scene':
                width = int(words[1])
                height = int(words[2])
                screen = pygame.display.set_mode((width, height))
                scene = Scene(width, height, SCENE_SPEED_INITIAL, screen)
            elif words[0] == 'SensorDrivenRobot':
                x = float(words[1])
                y = float(words[2])
                robot = SensorDrivenRobot(x, y, ROBOT_SIZE, ROBOT_WHEEL_RADIUS)
                robot.set_label(line_number)
                scene.put(robot)
            elif words[0] == 'Box':
                x = int(words[1])
                y = int(words[2])
                size = int(words[3])
                box = Box(x, y, size, Color.random_bright())
                box.set_label(line_number)
                scene.put(box)
            elif words[0] == 'Wall':
                x1 = int(words[1])
                y1 = int(words[2])
                x2 = int(words[3])
                y2 = int(words[4])

                point1 = Point(x1, y1)
                point2 = Point(x2, y2)
                wall = Wall(point1, point2, Color.random_bright())
                wall.set_label(line_number)
                scene.put(wall)

            line_number += 1

    f.closed
    boxes_added = []
    label = line_number


def add_box_to_cursor():
    global scene
    global boxes_added
    global label

    x, y = pygame.mouse.get_pos()
    size = random.randint(20, 60)
    box = Box(x, y, size, Color.random_bright())
    box.set_label(label)
    label += 1
    boxes_added.append(box)
    scene.put(box)


def remove_box():
    global scene
    global boxes_added
    global label

    if len(boxes_added) > 0:
        scene.remove(boxes_added.pop())
        label -= 1


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    init_scene()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_r:
                init_scene()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                add_box_to_cursor()
            elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                remove_box()
            elif event.type == KEYDOWN and event.key == K_s:
                scene.save()

        screen.fill(Color.BLACK)

        for obj in scene.objects:
            obj.draw(screen)

            # draw a label on the object
            if hasattr(obj, 'draw_label'):
                obj.draw_label(screen)

        pygame.display.flip()
        int_scene_speed = int(round(scene.speed))
        clock.tick(int_scene_speed)
