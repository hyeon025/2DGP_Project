from pico2d import load_image, draw_rectangle, draw_circle
import math
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

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
        self.bt = self.build_behavior_tree()

    def update(self):
        if not self.alive:
            return

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        if self.bt:
            self.bt.run()

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
                draw_circle(self.x, self.y, int(PIXEL_PER_METER * 7), 255, 255, 0)

    def handle_collision(self, group, other):
        pass

    def get_bb(self):
        return self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size

    def distance_less_than(self, x1, y1, x2, y2, r):

        distance2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def is_target_nearby(self, distance):
        if self.distance_less_than(self.x, self.y, self.target.x, self.target.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_target(self):
        if self.target is None:
            return BehaviorTree.FAIL

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

            if self.dir_x > 0:
                self.face_dir = 1
            elif self.dir_x < 0:
                self.face_dir = -1

            return BehaviorTree.SUCCESS
        else:
            self.dir_x = 0
            self.dir_y = 0
            return BehaviorTree.SUCCESS

    def idle(self):
        self.dir_x = 0
        self.dir_y = 0
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):

        c_near = Condition('가까이 있는가?', self.is_target_nearby, 7)
        a_move = Action('타겟으로 이동', self.move_to_target)
        chase_node = Sequence('플레이어 쫓아감',c_near,a_move)

        idle_node = Action('그냥 서있기', self.idle)

        root = Selector('몬스터 BT',chase_node,idle_node)

        return BehaviorTree(root)



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
        super().__init__(x, y, hp=500, size=100, target=target)
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
        self.attack_range = 100
        self.detection_range = 200
        self.attack_cooldown = 1.0
        self.post_attack_cooldown = 0
        self.state = 'idle'
        self.frame_speed = 0.5
        self.attack_finished = False

    def update(self):
        if not self.alive:
            return

        max_frames = self.sprite_info[self.state]['frames']

        if self.state == 'attack':
            prev_frame = int(self.frame)
            self.frame = self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * self.frame_speed

            if self.frame >= max_frames:
                self.frame = max_frames - 1
                if not self.attack_finished:
                    self.attack_finished = True
                    self.post_attack_cooldown = self.attack_cooldown
                    self.state = 'idle'
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * self.frame_speed) % max_frames

        if self.post_attack_cooldown > 0:
            self.post_attack_cooldown -= game_framework.frame_time

        if self.target is not None:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = math.hypot(dx, dy)

            if dx > 0:
                self.face_dir = 1
            elif dx < 0:
                self.face_dir = -1

            if self.state == 'attack' and not self.attack_finished:
                self.dir_x = 0
                self.dir_y = 0

            elif self.post_attack_cooldown > 0:
                self.state = 'idle'
                self.dir_x = 0
                self.dir_y = 0

            elif dist <= self.attack_range:
                self.state = 'attack'
                self.attack_finished = False
                self.frame = 0
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

                l2, b2, r2, t2 = self.get_hit_bb()
                sl2, sb2 = cam.to_camera(l2, b2)
                sr2, st2 = cam.to_camera(r2, t2)
                draw_rectangle(sl2, sb2, sr2, st2)
            else:
                draw_rectangle(*self.get_bb())
                draw_rectangle(*self.get_hit_bb())

    def get_bb(self):
        if self.state == 'attack' and 8 <= int(self.frame) <= 11:
            offset = self.face_dir * 80
            return self.x - self.size + offset + 50, self.y - self.size - 50, self.x + self.size + offset - 50, self.y + self.size - 50
        else:
            return self.x, self.y, self.x, self.y

    def get_hit_bb(self):
        return self.x - 60, self.y - 150, self.x + 60, self.y + 20