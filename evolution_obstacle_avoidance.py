import sys
import pygame
import util.cli_parser

from pygame.locals import *

from util.scene_type import SceneType
from util.side_panel import SidePanel
from util.color import Color
from scene.scene import Scene
from ga_obstacle_avoidance.ga_engine import GaEngine
from robot.sensor_driven_robot import SensorDrivenRobot
from util.time_util import TimeUtil


class EvolutionObstacleAvoidance:

    DEFAULT_SCENE_PATH = 'saved_scenes/obstacle_avoidance_900.txt'
    DEFAULT_SCENE_SPEED = 0  # 0 = maximum fps
    DEFAULT_VERBOSE_VALUE = 0  # 0, 1, 2
    SCENE_MAX_SPEED = 3000
    SIDE_PANEL_WIDTH = 480

    def __init__(self):
        self.scene = None
        self.screen = None
        self.engine = None
        self.side_panel = None
        self.population_num = None
        self.scene_speed = None
        self.scene_path = None
        self.elitism_num = None
        self.robot_random_direction = None
        self.multicore = None
        self.obstacle_sensor_error = None
        self.mutation_probability = None
        self.mutation_coefficient = None
        self.selection_ratio = None
        self.verbose = None

        self.parse_cli_arguments()
        pygame.init()
        pygame.display.set_caption("Obstacle avoidance evolution - BRAVE")
        clock = pygame.time.Clock()
        self.initialize()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_r:
                    self.initialize()
                elif event.type == KEYDOWN and (event.key == K_PLUS or event.key == 93 or event.key == 270):
                    self.increase_scene_speed()
                elif event.type == KEYDOWN and (event.key == K_MINUS or event.key == 47 or event.key == 269):
                    self.decrease_scene_speed()
                elif event.type == KEYDOWN and event.key == K_s:
                    self.engine.save_genomes()

            start_time = TimeUtil.current_time_millis()
            self.engine.step()
            end_time = TimeUtil.current_time_millis()
            step_duration = end_time - start_time
            self.printd(2, 'Step duration: ', step_duration)

            self.screen.fill(Color.BLACK)

            for obj in self.scene.objects:
                obj.draw(self.screen)

                if issubclass(type(obj), SensorDrivenRobot) and obj.label is not None:
                    obj.draw_label(self.screen)

            # draw a black background for the side panel
            side_panel_bg_rect = pygame.Rect(self.scene.width, 0, self.SIDE_PANEL_WIDTH, self.scene.height)
            pygame.draw.rect(self.screen, Color.BLACK, side_panel_bg_rect)

            self.side_panel.display_ga_info()

            pygame.display.flip()
            int_scene_speed = int(round(self.scene.speed))
            clock.tick(int_scene_speed)

    def initialize(self):
        self.scene = Scene.load_from_file(self.scene_path, self.scene_speed, self.SIDE_PANEL_WIDTH)
        self.screen = self.scene.screen
        self.side_panel = SidePanel(self.scene, self.population_num)
        self.engine = GaEngine(self.scene, self.side_panel, self.population_num, self.elitism_num, self.robot_random_direction, self.multicore,
                               self.obstacle_sensor_error, self.mutation_probability, self.mutation_coefficient, self.selection_ratio, self.verbose)

    def increase_scene_speed(self):
        if self.scene.speed < self.SCENE_MAX_SPEED:
            self.scene.speed *= 1.5

        print('Scene speed:', self.scene.speed)

    def decrease_scene_speed(self):
        if self.scene.speed == 0:
            self.scene.speed = self.SCENE_MAX_SPEED

        if self.scene.speed > 1:
            self.scene.speed /= 1.5

        print('Scene speed:', self.scene.speed)

    def parse_cli_arguments(self):
        parser = util.cli_parser.CliParser()
        parser.parse_args(self.DEFAULT_SCENE_PATH, self.DEFAULT_SCENE_SPEED, SceneType.GA_OBSTACLE_AVOIDANCE)

        self.elitism_num = parser.elitism_num
        self.population_num = parser.population_num
        self.mutation_probability = parser.mutation_probability
        self.mutation_coefficient = parser.mutation_coefficient
        self.robot_random_direction = parser.robot_random_direction
        self.scene_speed = parser.scene_speed
        self.scene_path = parser.scene_file
        self.obstacle_sensor_error = parser.obstacle_sensor_error
        self.selection_ratio = parser.selection_ratio
        self.multicore = parser.multicore
        self.verbose = parser.verbose

    def printd(self, min_debug_level, *args):
        if self.verbose >= min_debug_level:
            msg = ''

            for arg in args:
                msg += str(arg) + ' '

            print(msg)


if __name__ == '__main__':
    EvolutionObstacleAvoidance()
