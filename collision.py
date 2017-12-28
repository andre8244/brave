class Collision(Exception):

    def __init__(self, object1, object2):
        self.object1 = object1
        self.object2 = object2

