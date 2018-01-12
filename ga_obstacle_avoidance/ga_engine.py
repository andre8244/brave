from robot.sensor_driven_robot import SensorDrivenRobot


class GaEngine:

    def __init__(self, scene):
        self.scene = scene
        self.population = []

        for obj in scene.objects:
            if issubclass(type(obj), SensorDrivenRobot):
                self.population.append(obj)

    def step(self):
        # todo
        pass
