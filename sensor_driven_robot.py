from differential_drive_robot import DifferentialDriveRobot

class SensorDrivenRobot(DifferentialDriveRobot):

    def __init__(self, x, y, length, wheel_radius):
        super().__init__(x, y, length, wheel_radius)

    def sense_and_act(self):
        self.left_motor_controller.sense_and_act()
        self.right_motor_controller.sense_and_act()
        self.speed_left_wheel = self.left_motor_controller.get_actuator_value()
        self.speed_right_wheel = self.right_motor_controller.get_actuator_value()

    def set_left_motor_controller(self, left_motor_controller):
        self.left_motor_controller = left_motor_controller

    def set_right_motor_controller(self, right_motor_controller):
        self.right_motor_controller = right_motor_controller
