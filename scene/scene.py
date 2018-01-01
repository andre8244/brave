from time_util import TimeUtil


class Scene:

    def __init__(self, width, height, speed, screen):
        self.width = width
        self.height = height
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

    def save(self):
        file_name = "scene-" + str(TimeUtil.current_time_millis()) + ".txt"
        file_path = 'saved_scenes/' + file_name

        with open(file_path, 'w') as f:
            f.write(self.get_saved_scene_repr() + '\n')  # first line with scene size

            for obj in self.objects:
                if hasattr(obj, 'get_saved_scene_repr'):
                    line = obj.get_saved_scene_repr()
                    f.write(line + '\n')
                else:
                    print('Object unsaved:', obj)
        f.closed
        print('Scene saved:', file_path)

    def get_saved_scene_repr(self):
        return self.__class__.__name__ + ' ' + str(self.width) + ' ' + str(self.height)
