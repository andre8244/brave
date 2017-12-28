from differential_drive_robot import DifferentialDriveRobot
from collision import Collision


class SensorDrivenRobot(DifferentialDriveRobot):

    def __init__(self, x, y, length, wheel_radius):
        super().__init__(x, y, length, wheel_radius)
        self.collision_with_object = False

    def sense_and_act(self):
        if not self.collision_with_object:
            try:
                self.left_motor_controller.sense_and_act()
                self.right_motor_controller.sense_and_act()
                self.speed_left_wheel = self.left_motor_controller.get_actuator_value()
                self.speed_right_wheel = self.right_motor_controller.get_actuator_value()
            except Collision:
                self.collision_with_object = True
                self.speed_left_wheel = 0
                self.speed_right_wheel = 0
        else:
            # a collision has already occured
            self.speed_left_wheel = 0
            self.speed_right_wheel = 0

        self.step()

    def set_left_motor_controller(self, left_motor_controller):
        self.left_motor_controller = left_motor_controller

    def set_right_motor_controller(self, right_motor_controller):
        self.right_motor_controller = right_motor_controller

    def draw(self, screen):
        # draw the sensor lines
        self.left_motor_controller.sensor.draw()
        self.right_motor_controller.sensor.draw()
        # call super method to draw the robot
        super(SensorDrivenRobot, self).draw(screen)
