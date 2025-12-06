from pico2d import load_image, draw_rectangle
import game_framework
import game_world
import math

PIXEL_PER_METER = (10.0 / 0.3)
BULLET_SPEED_KMPH = 30.0
BULLET_SPEED_MPM = (BULLET_SPEED_KMPH * 1000.0 / 60.0)
BULLET_SPEED_MPS = (BULLET_SPEED_MPM / 60.0)
BULLET_SPEED_PPS = (BULLET_SPEED_MPS * PIXEL_PER_METER)

FRAMES_PER_ACTION = 4
ACTION_PER_TIME = 1.0


class Bomb:
    image = None

    def __init__(self, x, y, target_x, target_y, damage=10):
        self.x = x
        self.y = y
        self.damage = damage
        self.alive = True
        self.frame = 0

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

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

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

        self.image.clip_draw(int(self.frame) * 12, 0, 12, 12, sx, sy, 32, 32)

        if game_framework.show_bb:
            if cam:
                l, b, r, t = self.get_bb()
                sl, sb = cam.to_camera(l, b)
                sr, st = cam.to_camera(r, t)
                draw_rectangle(sl, sb, sr, st)
            else:
                draw_rectangle(*self.get_bb())

    def get_bb(self):
        if not self.alive:
            return 0, 0, 0, 0
        return self.x - 16, self.y - 16, self.x + 16, self.y + 16

    def handle_collision(self, group, other):
        if group == 'bullet:player':
            self.alive = False
        elif group == 'weapon:bullet':
            self.alive = False
            game_world.remove_object(self)
        elif group == 'skill:bullet':
            self.alive = False
            game_world.remove_object(self)


class BulletStone:
    image = None
    FRAME_WIDTH = 40
    FRAME_HEIGHT = 38
    TOTAL_FRAMES = 12
    FRAMES_PER_ROW = 6

    def __init__(self, x, y, target_x, target_y, damage=5):
        self.x = x
        self.y = y
        self.damage = damage
        self.alive = True
        self.frame = 0

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

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % BulletStone.TOTAL_FRAMES

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

        frame_index = int(self.frame)
        frame_x = (frame_index % BulletStone.FRAMES_PER_ROW) * BulletStone.FRAME_WIDTH
        frame_y = (frame_index // BulletStone.FRAMES_PER_ROW) * BulletStone.FRAME_HEIGHT

        self.image.clip_draw(frame_x, frame_y, BulletStone.FRAME_WIDTH, BulletStone.FRAME_HEIGHT, sx, sy, 24, 24)

        if game_framework.show_bb:
            if cam:
                l, b, r, t = self.get_bb()
                sl, sb = cam.to_camera(l, b)
                sr, st = cam.to_camera(r, t)
                draw_rectangle(sl, sb, sr, st)
            else:
                draw_rectangle(*self.get_bb())

    def get_bb(self):
        if not self.alive:
            return 0, 0, 0, 0
        return self.x - 12, self.y - 12, self.x + 12, self.y + 12

    def handle_collision(self, group, other):
        if group == 'bullet:player':
            self.alive = False
        elif group == 'weapon:bullet':
            self.alive = False
            game_world.remove_object(self)
        elif group == 'skill:bullet':
            self.alive = False
            game_world.remove_object(self)
