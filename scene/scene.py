class Scene:

    def __init__(self, speed, screen):
        self.speed = speed
        self.screen = screen
        self.objects = []

    def put(self, obj):
        if isinstance(obj, list):
            self.objects.extend(obj)
        else:
            self.objects.append(obj)

    def remove(self, obj):
        self.objects.remove(obj)
