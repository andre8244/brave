import pygame
import math

from geometry.color import Color
from time_util import TimeUtil


class Statistics:

    LINE_SPACING = 45
    DEFAULT_LEFT_MARGIN = 45

    def __init__(self, scene, screen, population_num):
        self.scene = scene
        self.screen = screen
        self.population_num = population_num
        self.generation_num = None
        self.best_genome = None
        self.fitness_best_genome = None
        self.total_time_seconds = None
        self.generation_time_seconds = None
        self.line_num = None

    def update_data(self, generation_num, best_genome, fitness_best_genome):
        self.generation_num = generation_num
        self.best_genome = best_genome
        self.fitness_best_genome = fitness_best_genome

    def update_time(self, total_time_seconds, generation_time_seconds):
        self.total_time_seconds = total_time_seconds
        self.generation_time_seconds = generation_time_seconds

    def show(self):
        if pygame.font:
            font = pygame.font.Font(None, 28)
            self.line_num = 1

            if self.best_genome is None:
                # this happens only in the first generation
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
            self.print_statistic(font, 'Fitness: ' + fitness_best, 80)
            self.print_statistic(font, 'Generation born: ' + generation_num_best, 80)
            self.print_statistic(font, 'Vehicle wheel radius: ' + robot_wheel_radius_best, 80)
            self.print_statistic(font, 'Motor ctrl coefficient: ' + motor_ctrl_coefficient_best, 80)
            self.print_statistic(font, 'Motor ctrl min actuator value: ' + motor_ctrl_min_actuator_value_best, 80)
            self.print_statistic(font, 'Sensor direction: ' + sensor_delta_direction_best_deg + ' deg (' +
                                 sensor_delta_direction_best_rad + ' rad)', 80)

            self.print_statistic(font, 'Sensor saturation value: ' + sensor_saturation_value_best, 80)
            self.print_statistic(font, 'Sensor max distance: ' + sensor_max_distance_best, 80)

    def print_statistic(self, font, text, left_margin=None):
        if left_margin is None:
            left_margin = self.DEFAULT_LEFT_MARGIN

        line = font.render(text, 1, Color.WHITE)
        lint_pos = pygame.Rect(self.scene.width + left_margin, self.line_num * self.LINE_SPACING, 20, 20)
        self.screen.blit(line, lint_pos)
        self.line_num += 1
