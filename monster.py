from pico2d import load_image, draw_rectangle
import math
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
    image = None
    def __init__(self,x,y,hp,size,target = None):
        self.x = x
        self.y = y
        self.frame = 0
        self.face_dir = 1
        self.dir_x = 0
        self.dir_y = 0
        self.hp = hp
        self.target = target
        self.alive = True
        self.size = size

    def update(self):
        if not self.alive:
            return

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        if self.target is not None:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 1:
                nx = dx / dist
                ny = dy / dist
                self.dir_x = nx
                self.dir_y = ny
                self.x += self.dir_x * RUN_SPEED_PPS * self.speed_factor * game_framework.frame_time
                self.y += self.dir_y * RUN_SPEED_PPS * self.speed_factor * game_framework.frame_time
            else:
                self.dir_x = 0
                self.dir_y = 0

        if self.dir_x > 0:
            self.face_dir = 1
        elif self.dir_x < 0:
            self.face_dir = -1

    def draw(self):
        cam = game_world.camera
        if cam:
            sx, sy = cam.to_camera(self.x, self.y)
        else:
            sx, sy = self.x, self.y

        if self.alive:
            if self.face_dir == 1:
                self.image.clip_draw(int(self.frame) * 24, 72, 24, 24, sx, sy, 40, 40)
            else:
                self.image.clip_composite_draw(int(self.frame) * 24, 72, 24, 24, 0, 'h', sx, sy, 40, 40)
        else:
            if self.face_dir == 1:
                self.image.clip_draw(0, 24, 24, 24, sx, sy, 40, 40)
            else:
                self.image.clip_composite_draw(0, 24, 24, 24, 0,'h',sx, sy, 40, 40)
        if game_framework.show_bb and self.alive:
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
        return self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size



class EggMonster(Monster):
    image = None

    def __init__(self, x, y,target=None):
        super().__init__(x, y, hp = 10, size = 12, target = target)
        if EggMonster.image is None:
            EggMonster.image = load_image('asset/Monster/egg.png')
        self.image = EggMonster.image
        self.size = 12
        self.speed_factor = 0.6

class AngryEggMonster(Monster):
    image = None

    def __init__(self, x, y,target=None):
        super().__init__(x, y, hp = 20, size = 12, target = target)
        if AngryEggMonster.image is None:
            AngryEggMonster.image = load_image('asset/Monster/angry_egg.png')
        self.image = AngryEggMonster.image
        self.speed_factor = 1.0

class Boss1(Monster):
    walk_image = None
    idle_image = None
    attack_image = None

    def __init__(self, x, y, target=None):
        super().__init__(x, y, hp=500, size=50, target=target)
        if Boss1.walk_image is None:
            Boss1.walk_image = load_image('asset/Monster/boss1_walk.png')
            Boss1.idle_image = load_image('asset/Monster/boss1_idle.png')
            Boss1.attack_image = load_image('asset/Monster/boss1_attack.png')

        self.sprite_info = {
            'walk': {'frames': 6, 'sx': 0, 'sy': 0, 'sw': 128, 'sh': 150, 'dw': 256, 'dh': 300, 'total_rows': 2},
            'idle': {'frames': 4, 'sx': 0, 'sy': 0, 'sw': 128, 'sh': 150, 'dw': 256, 'dh': 300, 'total_rows': 1},
            'attack': {'frames': 13, 'sx': 0, 'sy': 0, 'sw': 128, 'sh': 150, 'dw': 256, 'dh': 300, 'total_rows': 4}
        }

        self.speed_factor = 0.8
        self.attack_range = 75
        self.detection_range = 150
        self.attack_cooldown = 2.0
        self.attack_timer = 0
        self.state = 'idle'

    def update(self):
        if not self.alive:
            return

        max_frames = self.sprite_info[self.state]['frames']
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % max_frames

        if self.attack_timer > 0:
            self.attack_timer -= game_framework.frame_time

        if self.target is not None:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = math.hypot(dx, dy)

            if dx > 0:
                self.face_dir = 1
            elif dx < 0:
                self.face_dir = -1

            # attack 중일 때는 상태 변경 안 함 (attack_timer가 남아있으면 attack 지속)
            if self.state == 'attack' and self.attack_timer > 0:
                self.dir_x = 0
                self.dir_y = 0
            elif dist <= self.attack_range and self.attack_timer <= 0:
                self.state = 'attack'
                self.attack_timer = self.attack_cooldown
                self.frame = 0  # attack 시작 시 프레임 초기화
                self.dir_x = 0
                self.dir_y = 0
            elif dist <= self.detection_range:
                self.state = 'walk'
                nx = dx / dist
                ny = dy / dist
                self.dir_x = nx
                self.dir_y = ny
                self.x += self.dir_x * RUN_SPEED_PPS * self.speed_factor * game_framework.frame_time
                self.y += self.dir_y * RUN_SPEED_PPS * self.speed_factor * game_framework.frame_time
            else:
                self.state = 'idle'
                self.dir_x = 0
                self.dir_y = 0

    def draw(self):
        cam = game_world.camera
        if cam:
            sx, sy = cam.to_camera(self.x, self.y)
        else:
            sx, sy = self.x, self.y

        if self.state == 'walk':
            current_image = Boss1.walk_image
        elif self.state == 'idle':
            current_image = Boss1.idle_image
        else:
            current_image = Boss1.attack_image

        info = self.sprite_info[self.state]

        frame_col = int(self.frame) % 4
        frame_row = int(self.frame) // 4

        sprite_x = frame_col * info['sw'] + info['sx']
        sprite_y = (info['total_rows'] - 1 - frame_row) * info['sh'] + info['sy']

        if self.alive:
            if self.face_dir == 1:
                current_image.clip_draw(
                    sprite_x, sprite_y,
                    info['sw'], info['sh'],
                    sx, sy, info['dw'], info['dh']
                )
            else:
                current_image.clip_composite_draw(
                    sprite_x, sprite_y,
                    info['sw'], info['sh'],
                    0, 'h', sx, sy, info['dw'], info['dh']
                )
        else:
            if self.face_dir == 1:
                Boss1.walk_image.clip_draw(0, 0, 128, 150, sx, sy, 256, 300)
            else:
                Boss1.walk_image.clip_composite_draw(0, 0, 128, 150, 0, 'h', sx, sy, 256, 300)

        if game_framework.show_bb and self.alive:
            if cam:
                l, b, r, t = self.get_bb()
                sl, sb = cam.to_camera(l, b)
                sr, st = cam.to_camera(r, t)
                draw_rectangle(sl, sb, sr, st)
            else:
                draw_rectangle(*self.get_bb())