import math

from robot.sensor_driven_robot import SensorDrivenRobot


class GaRobot(SensorDrivenRobot):

    def __init__(self, x, y, length, genome):
        super().__init__(x, y, length, genome.robot_wheel_radius)
        self.genome = genome
        self.mileage = 0

    def step(self):
        super().step()
        distance = math.sqrt(math.pow(self.deltax, 2) + math.pow(self.deltay, 2))
        # print('mileage', self.mileage, 'deltax', self.deltax, 'deltay', self.deltay, 'distance', distance)
        self.mileage += distance
