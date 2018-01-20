import sys
import pygame

from pygame.locals import *
from geometry.color import Color
from scene.scene import Scene
from ga_obstacle_avoidance.ga_engine import GaEngine
from robot.sensor_driven_robot import SensorDrivenRobot


SCENE_MAX_SPEED = 2000
SCENE_SPEED_INITIAL = 2000
POPULATION_NUM = 500

scene = None
screen = None
engine = None


def initialize():
    global scene
    global screen
    global engine

    scene, screen = Scene.load_from_file('saved_scenes/scene_training_obstacle_avoidance.txt', SCENE_SPEED_INITIAL)
    engine = GaEngine(scene, POPULATION_NUM)


def increase_scene_speed():
    global scene

    if scene.speed < SCENE_MAX_SPEED:
        scene.speed *= 1.5
    print('scene.speed:', scene.speed)


def decrease_scene_speed():
    global scene

    if scene.speed > 1:
        scene.speed /= 1.5
    print('scene.speed:', scene.speed)


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    initialize()

    while True:
        for event in pygame.event.get():

            # if event.type == KEYDOWN:
            #     print('event.key', event.key) # todo del
            #     print('k_plus', K_PLUS)
            #     print('k_minus', K_MINUS)

            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_r:
                initialize()
            elif event.type == KEYDOWN and (event.key == K_PLUS or event.key == 93):
                increase_scene_speed()
            elif event.type == KEYDOWN and (event.key == K_MINUS or event.key == 47):
                decrease_scene_speed()
            # elif event.type == KEYDOWN and event.key == K_s:
            #     scene.save()

        engine.step()

        screen.fill(Color.BLACK)

        for obj in scene.objects:
            obj.draw(screen)

            if issubclass(type(obj), SensorDrivenRobot) and obj.label is not None:
                obj.draw_label(screen)

        pygame.display.flip()
        int_scene_speed = int(round(scene.speed))
        clock.tick(int_scene_speed)
