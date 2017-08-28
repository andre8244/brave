class Sensor():

    def __init__(self, robot, delta_direction, saturation_value, scene):
        self.robot = robot
        self.delta_direction =  delta_direction
        self.saturation_value = saturation_value
        self.scene = scene
        self.value = 0

    def get_value(self):
        # defined by subclasses
        pass
