from pico2d import load_image, draw_rectangle
import game_world
import game_framework
import random

class Box:
    images = None

    def __init__(self, x, y):
        if Box.images is None:
            Box.images = {
                1: {
                    'closed': load_image('asset/box/box_01.png'),
                    'opened': load_image('asset/box/open_box_01.png')
                },
                2: {
                    'closed': load_image('asset/box/box_02.png'),
                    'opened': load_image('asset/box/open_box_02.png')
                },
                3: {
                    'closed': load_image('asset/box/box_03.png'),
                    'opened': load_image('asset/box/open_box_03.png')
                }
            }
        self.x = x
        self.y = y
        self.opened = False
        self.box_type = random.randint(1, 3)

    def update(self):
        pass

    def open(self):
        self.opened = True

    def draw(self):
        cam = game_world.camera
        if cam:
            sx, sy = cam.to_camera(self.x, self.y)
        else:
            sx, sy = self.x, self.y

        if self.opened:
            Box.images[self.box_type]['opened'].draw(sx, sy, 120, 120)
        else:
            Box.images[self.box_type]['closed'].draw(sx, sy, 120, 120)

        if game_framework.show_bb:
            if cam:
                l, b, r, t = self.get_bb()
                sl, sb = cam.to_camera(l, b)
                sr, st = cam.to_camera(r, t)
                draw_rectangle(sl, sb, sr, st)
            else:
                draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 30

    def handle_collision(self, group, other):
        pass
