import pygame
import math

from util.color import Color
from util.time_util import TimeUtil


class SidePanel:

    FONT_SIZE = 30
    LINE_SPACING_MIN = 25
    LINE_SPACING_MAX = 35
    SCENE_HEIGHT_THRESHOLD = 700
    DEFAULT_MARGIN = 35
    LEFT_MARGIN = 30

    def __init__(self, scene, population_num=0):
        self.scene = scene
        self.screen = scene.screen
        self.population_num = population_num
        self.generation_num = None
        self.best_genome = None
        self.fitness_best_genome = None
        self.total_time_seconds = None
        self.generation_time_seconds = None
        self.line_num = None
        self.line_spacing = None

    def update_ga_data(self, generation_num, best_genome, fitness_best_genome):
        self.generation_num = generation_num
        self.best_genome = best_genome
        self.fitness_best_genome = fitness_best_genome

    def update_ga_time(self, total_time_seconds, generation_time_seconds):
        self.total_time_seconds = total_time_seconds
        self.generation_time_seconds = generation_time_seconds

    def display_ga_info(self):
        pygame.draw.line(self.screen, Color.GRAY, (self.scene.width, 0), (self.scene.width, self.scene.height))

        if pygame.font:
            font = pygame.font.Font(None, self.FONT_SIZE)
            self.line_num = 1

            if self.scene.height > self.SCENE_HEIGHT_THRESHOLD:
                self.line_spacing = self.LINE_SPACING_MAX
            else:
                self.line_spacing = self.LINE_SPACING_MIN

            if self.best_genome is None:
                # this happens only at the first generation
                fitness_best = '-'
                generation_num_best = '-'
                robot_wheel_radius_best = '-'
                motor_ctrl_coefficient_best = '-'
                motor_ctrl_min_actuator_value_best = '-'
                sensor_delta_direction_best_deg = '-'
                sensor_delta_direction_best_rad = '-'
                sensor_saturation_value_best = '-'
                sensor_max_distance_best = '-'
            else:
                fitness_best = str(round(self.fitness_best_genome, 2))
                generation_num_best = str(self.best_genome.generation_num)
                robot_wheel_radius_best = str(round(self.best_genome.robot_wheel_radius, 2))
                motor_ctrl_coefficient_best = str(round(self.best_genome.motor_ctrl_coefficient, 2))
                motor_ctrl_min_actuator_value_best = str(
                    round(self.best_genome.motor_ctrl_min_actuator_value, 2))
                sensor_delta_direction_best_deg = str(round(math.degrees(self.best_genome.sensor_delta_direction), 2))
                sensor_delta_direction_best_rad = str(round(self.best_genome.sensor_delta_direction, 2))
                sensor_saturation_value_best = str(round(self.best_genome.sensor_saturation_value, 2))
                sensor_max_distance_best = str(round(self.best_genome.sensor_max_distance, 2))

            total_time = TimeUtil.format_time_seconds(self.total_time_seconds)
            generation_time = TimeUtil.format_time_seconds(self.generation_time_seconds)

            self.print_statistic(font, 'Generation: ' + str(self.generation_num))
            self.print_statistic(font, 'Population: ' + str(self.population_num))
            self.print_statistic(font, 'Total time: ' + total_time)
            self.print_statistic(font, 'Generation time: ' + generation_time)

            self.print_statistic(font, 'Best genome:')
            self.print_statistic(font, 'Fitness: ' + fitness_best, self.LEFT_MARGIN)
            self.print_statistic(font, 'Generation born: ' + generation_num_best, self.LEFT_MARGIN)
            self.print_statistic(font, 'Wheel radius: ' + robot_wheel_radius_best, self.LEFT_MARGIN)
            self.print_statistic(font, 'Motor ctrl coefficient: ' + motor_ctrl_coefficient_best, self.LEFT_MARGIN)
            self.print_statistic(font, 'Motor ctrl min actuator value: ' + motor_ctrl_min_actuator_value_best,
                                 self.LEFT_MARGIN)
            self.print_statistic(font, 'Sensor direction: ' + sensor_delta_direction_best_deg + ' deg (' +
                                 sensor_delta_direction_best_rad + ' rad)', self.LEFT_MARGIN)

            self.print_statistic(font, 'Sensor saturation value: ' + sensor_saturation_value_best, self.LEFT_MARGIN)
            self.print_statistic(font, 'Sensor max distance: ' + sensor_max_distance_best, self.LEFT_MARGIN)

            # controls

            self.print_statistic(font, 'Controls:')
            self.print_statistic(font, 'S : save current genomes to file', self.LEFT_MARGIN)
            self.print_statistic(font, '+ : incrase scene speed', self.LEFT_MARGIN)
            self.print_statistic(font, '- : decrase scene speed', self.LEFT_MARGIN)
            self.print_statistic(font, 'R : restart', self.LEFT_MARGIN)
            self.print_statistic(font, 'ESC : quit', self.LEFT_MARGIN)

    def display_info(self, object_to_place):
        pygame.draw.line(self.screen, Color.GRAY, (self.scene.width, 0), (self.scene.width, self.scene.height))

        if pygame.font:
            font = pygame.font.Font(None, self.FONT_SIZE)
            self.line_num = 1
            self.line_spacing = self.LINE_SPACING_MAX

            self.print_statistic(font, 'Controls:')
            self.print_statistic(font, 'Click left : place ' + object_to_place, self.LEFT_MARGIN)
            self.print_statistic(font, 'Click right : remove ' + object_to_place, self.LEFT_MARGIN)
            self.print_statistic(font, 'J : add a vehicle', self.LEFT_MARGIN)
            self.print_statistic(font, 'K : remove a vehicle', self.LEFT_MARGIN)
            self.print_statistic(font, 'S : save current scene to file', self.LEFT_MARGIN)
            self.print_statistic(font, '+ : incrase scene speed', self.LEFT_MARGIN)
            self.print_statistic(font, '- : decrase scene speed', self.LEFT_MARGIN)
            self.print_statistic(font, 'R : restart', self.LEFT_MARGIN)
            self.print_statistic(font, 'ESC : quit', self.LEFT_MARGIN)

    def print_statistic(self, font, text, extra_margin=0):
            line = font.render(text, 1, Color.WHITE)
            x_pos = self.scene.width + self.DEFAULT_MARGIN + extra_margin
            y_pos = self.line_num * self.line_spacing
            lint_pos = pygame.Rect(x_pos, y_pos, 20, 20)
            self.screen.blit(line, lint_pos)
            self.line_num += 1
