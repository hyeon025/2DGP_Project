from pico2d import load_image
import game_framework
import game_world

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Monster:
    def __init__(self,x,y,hp):
        self.x = x
        self.y = y
        self.frame = 0
        self.face_dir = 1
        self.dir_x = 0
        self.dir_y = 0
        self.hp = hp
        self.alive = True

        self.image = load_image('asset/Monster/egg.png')
    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        self.x += self.dir_x * RUN_SPEED_PPS * game_framework.frame_time
        self.y += self.dir_y * RUN_SPEED_PPS * game_framework.frame_time

        if self.dir_x > 0:
            self.face_dir = 1
        elif self.dir_x < 0:
            self.face_dir = -1

    def draw(self):
        if not self.alive:
            return

        cam = game_world.camera
        if cam:
            sx, sy = cam.to_camera(self.x, self.y)
        else:
            sx, sy = self.x, self.y

        if self.face_dir == 1:
            self.image.clip_draw(int(self.frame) * 24, 48, 24, 24, sx, sy, 40, 40)
        else:
            self.image.clip_composite_draw(int(self.frame) * 24, 48, 24, 24, 0, 'h', sx, sy, 40, 40)

        if game_framework.show_bb:
            if cam:
                l, b, r, t = self.get_bb()
                sl, sb = cam.to_camera(l, b)
                sr, st = cam.to_camera(r, t)
                draw_rectangle(sl, sb, sr, st)
            else:
                draw_rectangle(*self.get_bb())

    def handle_collision(self, group, other):
        pass

    def get_bb(self):
        return self.x - 12, self.y - 12, self.x + 12, self.y + 12


