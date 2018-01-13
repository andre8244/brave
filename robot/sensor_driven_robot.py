import pygame

from robot.differential_drive_robot import DifferentialDriveRobot
from exception.collision_exception import Collision
from color import Color


class SensorDrivenRobot(DifferentialDriveRobot):

    def __init__(self, x, y, length, wheel_radius):
        super().__init__(x, y, length, wheel_radius)
        self.collision_with_object = False
        self.left_motor_controller = None
        self.right_motor_controller = None
        self.label = None

    def sense_and_act(self):
        if not self.collision_with_object:
            try:
                self.left_motor_controller.sense_and_act()
                self.right_motor_controller.sense_and_act()
                self.speed_left_wheel = self.left_motor_controller.get_actuator_value()
                self.speed_right_wheel = self.right_motor_controller.get_actuator_value()
                self.step()
            except Collision:
                self.collision_with_object = True
                self.speed_left_wheel = 0
                self.speed_right_wheel = 0
        else:
            # a collision has already occured
            self.speed_left_wheel = 0
            self.speed_right_wheel = 0

    def set_left_motor_controller(self, left_motor_controller):
        self.left_motor_controller = left_motor_controller

    def set_right_motor_controller(self, right_motor_controller):
        self.right_motor_controller = right_motor_controller

    def draw(self, screen):
        # draw the sensor lines

        # in scene_loader a robot doesn't have sensors
        if self.left_motor_controller is not None:
            self.left_motor_controller.sensor.draw()
            self.right_motor_controller.sensor.draw()

        # call super method to draw the robot
        super().draw(screen)

    # todo delete
    # def get_saved_scene_repr(self):
    #     return self.__class__.__name__ + ' ' + str(self.x) + ' ' + str(self.y)

    def set_label(self, label):
        self.label = label

    def draw_label(self, screen):
        if pygame.font:
            font = pygame.font.Font(None, 26)
            text = font.render(str(self.label), 1, Color.YELLOW, Color.DARK_GRAY)
            text_pos = pygame.Rect(self.x + (self.length / 2), self.y + (self.length / 2), 50, 50)
            screen.blit(text, text_pos)
