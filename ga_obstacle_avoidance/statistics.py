import pygame
import math

from geometry.color import Color


class Statistics:

    def __init__(self, scene, screen):
        self.scene = scene
        self.screen = screen
        self.generation_num = None
        self.best_genome = None
        self.fitness_best_genome = None

    def update(self, generation_num, best_genome, fitness_best_genome):
        self.generation_num = generation_num
        self.best_genome = best_genome
        self.fitness_best_genome = fitness_best_genome

    def show(self):
        if pygame.font:
            font = pygame.font.Font(None, 28)
            line1 = font.render('Generation: ' + str(self.generation_num), 1, Color.WHITE)
            line1_pos = pygame.Rect(self.scene.width + 50, 50, 20, 20)
            self.screen.blit(line1, line1_pos)

            if self.best_genome is not None:
                line2 = font.render('Best fitness: ' + str(round(self.fitness_best_genome, 2)), 1, Color.WHITE)
                line2_pos = pygame.Rect(self.scene.width + 50, 150, 20, 20)
                self.screen.blit(line2, line2_pos)

                line3 = font.render(
                    'Generation of best genome: ' + str(round(self.best_genome.generation_num)), 1, Color.WHITE)
                line3_pos = pygame.Rect(self.scene.width + 50, 250, 20, 20)
                self.screen.blit(line3, line3_pos)

                line4 = font.render('Best genome:', 1, Color.WHITE)
                line4_pos = pygame.Rect(self.scene.width + 50, 350, 20, 20)
                self.screen.blit(line4, line4_pos)

                line5 = font.render('     Robot wheel radius: ' + str(round(self.best_genome.robot_wheel_radius, 2)), 1,
                                    Color.WHITE)
                line5_pos = pygame.Rect(self.scene.width + 50, 400, 20, 20)
                self.screen.blit(line5, line5_pos)

                line6 = font.render(
                    '     Motor ctrl coefficient: ' + str(round(self.best_genome.motor_ctrl_coefficient, 2)),
                    1, Color.WHITE)
                line6_pos = pygame.Rect(self.scene.width + 50, 450, 20, 20)
                self.screen.blit(line6, line6_pos)

                line7 = font.render(
                    '     Motor ctrl min actuator value: ' + str(
                        round(self.best_genome.motor_ctrl_min_actuator_value, 2)), 1, Color.WHITE)
                line7_pos = pygame.Rect(self.scene.width + 50, 500, 20, 20)
                self.screen.blit(line7, line7_pos)

                line8 = font.render(
                    '     Sensor direction: ' + str(
                        round(math.degrees(self.best_genome.sensor_delta_direction), 2)) + '°', 1, Color.WHITE)
                line8_pos = pygame.Rect(self.scene.width + 50, 550, 20, 20)
                self.screen.blit(line8, line8_pos)

                line9 = font.render(
                    '     Sensor saturation value: ' + str(round(self.best_genome.sensor_saturation_value, 2)), 1,
                    Color.WHITE)
                line9_pos = pygame.Rect(self.scene.width + 50, 600, 20, 20)
                self.screen.blit(line9, line9_pos)

                line10 = font.render('     Sensor max distance: ' + str(round(self.best_genome.sensor_max_distance, 2)),
                                     1, Color.WHITE)
                line10_pos = pygame.Rect(self.scene.width + 50, 650, 20, 20)
                self.screen.blit(line10, line10_pos)
