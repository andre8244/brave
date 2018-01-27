import sys
import pygame
import math

from pygame.locals import *
from geometry.color import Color
from scene.scene import Scene
from ga_obstacle_avoidance.ga_engine import GaEngine
from robot.sensor_driven_robot import SensorDrivenRobot
from time_util import TimeUtil


POPULATION_NUM = 300
SCENE_MAX_SPEED = 2000
SCENE_SPEED_INITIAL = 2000  # 2000

scene = None
screen = None
engine = None


def initialize():
    global scene
    global screen
    global engine

    scene, screen = Scene.load_from_file('saved_scenes/scene_training_obstacle_avoidance.txt', SCENE_SPEED_INITIAL)

    # redefine pygame screen in order to display statistics
    screen_width = scene.width + 500
    screen_height = scene.height
    screen = pygame.display.set_mode((screen_width, screen_height))
    scene.screen = screen

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


def show_statistics():
    global screen
    global engine
    global scene

    if pygame.font:
        font = pygame.font.Font(None, 28)
        line1 = font.render('Generation: ' + str(engine.generation_num), 1, Color.WHITE)
        line1_pos = pygame.Rect(scene.width + 50, 50, 20, 20)
        screen.blit(line1, line1_pos)

        best_genome = engine.best_genome

        if best_genome is not None:
            line2 = font.render('Best fitness: ' + str(round(best_genome.fitness, 2)), 1, Color.WHITE)
            line2_pos = pygame.Rect(scene.width + 50, 150, 20, 20)
            screen.blit(line2, line2_pos)

            line3 = font.render(
                'Generation of best genome: ' + str(round(best_genome.generation_num)), 1, Color.WHITE)
            line3_pos = pygame.Rect(scene.width + 50, 250, 20, 20)
            screen.blit(line3, line3_pos)

            line4 = font.render('Best genome:', 1, Color.WHITE)
            line4_pos = pygame.Rect(scene.width + 50, 350, 20, 20)
            screen.blit(line4, line4_pos)

            line5 = font.render('     Robot wheel radius: ' + str(round(best_genome.robot_wheel_radius, 2)), 1,
                                Color.WHITE)
            line5_pos = pygame.Rect(scene.width + 50, 400, 20, 20)
            screen.blit(line5, line5_pos)

            line6 = font.render('     Motor ctrl coefficient: ' + str(round(best_genome.motor_ctrl_coefficient, 2)),
                                1, Color.WHITE)
            line6_pos = pygame.Rect(scene.width + 50, 450, 20, 20)
            screen.blit(line6, line6_pos)

            line7 = font.render(
                '     Motor ctrl min actuator value: ' + str(round(best_genome.motor_ctrl_min_actuator_value, 2)), 1,
                Color.WHITE)
            line7_pos = pygame.Rect(scene.width + 50, 500, 20, 20)
            screen.blit(line7, line7_pos)

            line8 = font.render(
                '     Sensor direction: ' + str(round(math.degrees(best_genome.sensor_delta_direction), 2)) + '°', 1,
                Color.WHITE)
            line8_pos = pygame.Rect(scene.width + 50, 550, 20, 20)
            screen.blit(line8, line8_pos)

            line9 = font.render('     Sensor saturation value: ' + str(round(best_genome.sensor_saturation_value, 2)),
                                1, Color.WHITE)
            line9_pos = pygame.Rect(scene.width + 50, 600, 20, 20)
            screen.blit(line9, line9_pos)

            line10 = font.render('     Sensor max distance: ' + str(round(best_genome.sensor_max_distance, 2)), 1,
                                 Color.WHITE)
            line10_pos = pygame.Rect(scene.width + 50, 650, 20, 20)
            screen.blit(line10, line10_pos)


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    initialize()

    while True:
        for event in pygame.event.get():
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

        start_time = TimeUtil.current_time_millis()
        engine.step()
        end_time = TimeUtil.current_time_millis()
        step_duration = end_time - start_time
        print('total step duration', step_duration)

        screen.fill(Color.BLACK)

        for obj in scene.objects:
            obj.draw(screen)

            if issubclass(type(obj), SensorDrivenRobot) and obj.label is not None:
                obj.draw_label(screen)

        show_statistics()

        pygame.display.flip()
        int_scene_speed = int(round(scene.speed))
        clock.tick(int_scene_speed)
