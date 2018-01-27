import threading


class ThreadGaRobot(threading.Thread):

    def __init__(self, robots):
        threading.Thread.__init__(self)
        self.robots = robots

    def run(self):
        # print('thread', self.name, 'with', len(self.robots), 'robots')

        for robot in self.robots:
            robot.sense_and_act()
