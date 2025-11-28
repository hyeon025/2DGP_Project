from pico2d import load_image, draw_rectangle
import game_framework
import game_world
import math

PIXEL_PER_METER = (10.0 / 0.3)
BULLET_SPEED_KMPH = 30.0
BULLET_SPEED_MPM = (BULLET_SPEED_KMPH * 1000.0 / 60.0)
BULLET_SPEED_MPS = (BULLET_SPEED_MPM / 60.0)
BULLET_SPEED_PPS = (BULLET_SPEED_MPS * PIXEL_PER_METER)


class Bomb:
    image = None

    def __init__(self, x, y, target_x, target_y, damage=10):
        self.x = x
        self.y = y
        self.damage = damage
        self.alive = True

        if Bomb.image is None:
            Bomb.image = load_image('asset/attack/bomb.png')

        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)

        if dist > 0:
            self.dir_x = dx / dist
            self.dir_y = dy / dist
        else:
            self.dir_x = 1
            self.dir_y = 0

        self.lifetime = 3.0

    def update(self):
        if not self.alive:
            return

        self.x += self.dir_x * BULLET_SPEED_PPS * game_framework.frame_time
        self.y += self.dir_y * BULLET_SPEED_PPS * game_framework.frame_time

        self.lifetime -= game_framework.frame_time
        if self.lifetime <= 0:
            self.alive = False
            game_world.remove_object(self)

    def draw(self):
        if not self.alive:
            return

        cam = game_world.camera
        if cam:
            sx, sy = cam.to_camera(self.x, self.y)
        else:
            sx, sy = self.x, self.y

        self.image.draw(sx, sy, 32, 32)

        if game_framework.show_bb:
            if cam:
                l, b, r, t = self.get_bb()
                sl, sb = cam.to_camera(l, b)
                sr, st = cam.to_camera(r, t)
                draw_rectangle(sl, sb, sr, st)
            else:
                draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 16, self.y - 16, self.x + 16, self.y + 16

    def handle_collision(self, group, other):
        if group == 'bullet:monster':
            self.alive = False


class BulletStone:
    image = None

    def __init__(self, x, y, target_x, target_y, damage=5):
        self.x = x
        self.y = y
        self.damage = damage
        self.alive = True

        if BulletStone.image is None:
            BulletStone.image = load_image('asset/attack/bullet_stone.png')

        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)

        if dist > 0:
            self.dir_x = dx / dist
            self.dir_y = dy / dist
        else:
            self.dir_x = 1
            self.dir_y = 0

        self.lifetime = 2.0

    def update(self):
        if not self.alive:
            return

        self.x += self.dir_x * BULLET_SPEED_PPS * game_framework.frame_time
        self.y += self.dir_y * BULLET_SPEED_PPS * game_framework.frame_time

        self.lifetime -= game_framework.frame_time
        if self.lifetime <= 0:
            self.alive = False
            game_world.remove_object(self)

    def draw(self):
        if not self.alive:
            return

        cam = game_world.camera
        if cam:
            sx, sy = cam.to_camera(self.x, self.y)
        else:
            sx, sy = self.x, self.y

        self.image.draw(sx, sy, 24, 24)

        if game_framework.show_bb:
            if cam:
                l, b, r, t = self.get_bb()
                sl, sb = cam.to_camera(l, b)
                sr, st = cam.to_camera(r, t)
                draw_rectangle(sl, sb, sr, st)
            else:
                draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 12, self.y - 12, self.x + 12, self.y + 12

    def handle_collision(self, group, other):
        if group == 'bullet:monster':
            self.alive = False
