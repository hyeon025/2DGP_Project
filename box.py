from pico2d import load_image, draw_rectangle
import game_world
import game_framework

class Box:
    image = None

    def __init__(self, x, y):
        if Box.image is None:
            Box.image = load_image('asset/box/box_01.png')
        self.image = Box.image
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self):
        cam = game_world.camera
        if cam:
            sx, sy = cam.to_camera(self.x, self.y)
        else:
            sx, sy = self.x, self.y

        self.image.draw(sx, sy, 120, 120)

        if game_framework.show_bb:
            if cam:
                l, b, r, t = self.get_bb()
                sl, sb = cam.to_camera(l, b)
                sr, st = cam.to_camera(r, t)
                draw_rectangle(sl, sb, sr, st)
            else:
                draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 60, self.y - 60, self.x + 60, self.y + 60

    def handle_collision(self, group, other):
        pass
