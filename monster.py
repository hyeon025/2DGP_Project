from pico2d import load_image, draw_rectangle, draw_circle
from PIL import Image
import math
import random
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from bullet import Bomb

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

_collision_data = None
_collision_width = 0
_collision_height = 0
_image_mode = None

def load_collision_map():
    global _collision_data, _collision_width, _collision_height, _image_mode

    if _collision_data is None:
        img = Image.open('asset/Map/round1_close_collision.png')
        _collision_data = img.load()
        _collision_width = img.width
        _collision_height = img.height
        _image_mode = img.mode

def is_valid_position(x, y, margin_meters=1):
    global _collision_data, _collision_width, _collision_height, _image_mode

    load_collision_map()

    scale = 10000.0 / _collision_width
    margin_pixels = int(PIXEL_PER_METER * margin_meters)

    check_points = [
        (x, y),
        (x + margin_pixels, y),
        (x - margin_pixels, y),
        (x, y + margin_pixels),
        (x, y - margin_pixels),
        (x + margin_pixels, y + margin_pixels),
        (x - margin_pixels, y + margin_pixels),
        (x + margin_pixels, y - margin_pixels),
        (x - margin_pixels, y - margin_pixels),
    ]

    for px, py in check_points:
        img_x = int(px / scale)
        img_y = int(py / scale)

        if img_x < 0 or img_x >= _collision_width or img_y < 0 or img_y >= _collision_height:
            return False

        pil_y = _collision_height - 1 - img_y
        pixel = _collision_data[img_x, pil_y]

        if _image_mode == 'L':
            r = g = b = pixel
        elif _image_mode == 'RGB':
            r, g, b = pixel
        elif _image_mode == 'RGBA':
            r, g, b, a = pixel
        else:
            r = g = b = pixel if isinstance(pixel, int) else pixel[0]

        if r < 1 and g < 1 and b < 1:
            return False

    return True

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
        self.speed_factor = 1.0
        self.random_target_x = x
        self.random_target_y = y
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

                if self.target:
                    tx, ty = cam.to_camera(self.target.x, self.target.y)
                    draw_circle(int(tx), int(ty), int(PIXEL_PER_METER * 7), 255, 255, 0)
            else:
                draw_rectangle(*self.get_bb())
                if self.target:
                    draw_circle(int(self.target.x), int(self.target.y), int(PIXEL_PER_METER * 7), 255, 255, 0)

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

    def set_random_target(self):
        TWO_METERS = int(PIXEL_PER_METER * 2)
        MAX_ATTEMPTS = 20

        for _ in range(MAX_ATTEMPTS):
            offset_x = random.randint(-TWO_METERS, TWO_METERS)
            offset_y = random.randint(-TWO_METERS, TWO_METERS)

            candidate_x = self.x + offset_x
            candidate_y = self.y + offset_y

            if is_valid_position(candidate_x, candidate_y, margin_meters=1):
                self.random_target_x = candidate_x
                self.random_target_y = candidate_y
                return BehaviorTree.SUCCESS

        self.random_target_x = self.x
        self.random_target_y = self.y
        return BehaviorTree.SUCCESS

    def move_to_random_position(self):
        dx = self.random_target_x - self.x
        dy = self.random_target_y - self.y
        dist = math.hypot(dx, dy)

        if dist > 10:
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

            return BehaviorTree.RUNNING
        else:
            self.dir_x = 0
            self.dir_y = 0
            return BehaviorTree.SUCCESS

    def build_behavior_tree(self):

        c_near = Condition('가까이 있는가?', self.is_target_nearby, 7)
        a_move = Action('타겟으로 이동', self.move_to_target)
        chase_node = Sequence('플레이어 쫓아감',c_near,a_move)

        wander_node = Sequence('랜덤 배회',Action('랜덤 위치 설정', self.set_random_target),Action('랜덤 위치로 이동', self.move_to_random_position))

        root = Selector('몬스터 BT',chase_node,wander_node)

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
        self.sprite_info = {
            'walk': {'frames': 6, 'sx': 0, 'sy': 0, 'sw': 128, 'sh': 150, 'dw': 256, 'dh': 300, 'total_rows': 2},
            'idle': {'frames': 4, 'sx': 0, 'sy': 0, 'sw': 128, 'sh': 150, 'dw': 256, 'dh': 300, 'total_rows': 1},
            'attack': {'frames': 13, 'sx': 0, 'sy': 0, 'sw': 128, 'sh': 150, 'dw': 256, 'dh': 300, 'total_rows': 4}
        }

        self.speed_factor = 0.8
        self.attack_range = int(PIXEL_PER_METER * 3)
        self.detection_range = int(PIXEL_PER_METER * 7)
        self.attack_cooldown = 1.0
        self.post_attack_cooldown = 0
        self.state = 'idle'
        self.frame_speed = 0.5
        self.attack_finished = False
        self.bomb_cooldown = 5.0
        self.bomb_timer = 0
        self.is_shooting_bomb = False
        self.bomb_shoot_delay = 1.0
        self.bomb_shoot_timer = 0

        super().__init__(x, y, hp=500, size=100, target=target)

        if Boss1.walk_image is None:
            Boss1.walk_image = load_image('asset/Monster/boss1_walk.png')
            Boss1.idle_image = load_image('asset/Monster/boss1_idle.png')
            Boss1.attack_image = load_image('asset/Monster/boss1_attack.png')

    def get_center_pos(self):
        return self.x, self.y - 80

    def is_attack_range(self):
        if self.target is None:
            return BehaviorTree.FAIL
        cx, cy = self.get_center_pos()
        dx = self.target.x - cx
        dy = self.target.y - cy
        dist = math.hypot(dx, dy)
        if dist <= self.attack_range:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_detection_range(self):
        if self.target is None:
            return BehaviorTree.FAIL
        cx, cy = self.get_center_pos()
        dx = self.target.x - cx
        dy = self.target.y - cy
        dist = math.hypot(dx, dy)
        if dist <= self.detection_range:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def do_attack(self):
        if self.post_attack_cooldown > 0:
            self.state = 'idle'
            return BehaviorTree.FAIL

        if self.state != 'attack' or self.attack_finished:
            self.state = 'attack'
            self.attack_finished = False
            self.frame = 0

        self.dir_x = 0
        self.dir_y = 0

        if self.target:
            cx, cy = self.get_center_pos()
            dx = self.target.x - cx
            if dx > 0:
                self.face_dir = 1
            elif dx < 0:
                self.face_dir = -1

        if self.attack_finished:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def move_to_target_boss(self):
        if self.target is None:
            return BehaviorTree.FAIL

        self.state = 'walk'

        cx, cy = self.get_center_pos()
        dx = self.target.x - cx
        dy = self.target.y - cy
        dist = math.hypot(dx, dy)

        if dist > 1:
            nx = dx / dist
            ny = dy / dist
            self.dir_x = nx
            self.dir_y = ny

            new_x = self.x + self.dir_x * RUN_SPEED_PPS * self.speed_factor * game_framework.frame_time
            new_y = self.y + self.dir_y * RUN_SPEED_PPS * self.speed_factor * game_framework.frame_time

            if is_valid_position(new_x, new_y, margin_meters=1):
                self.x = new_x
                self.y = new_y

            if self.dir_x > 0:
                self.face_dir = 1
            elif self.dir_x < 0:
                self.face_dir = -1

            return BehaviorTree.SUCCESS
        else:
            self.dir_x = 0
            self.dir_y = 0
            return BehaviorTree.SUCCESS

    def boss_idle(self):
        self.state = 'idle'
        self.dir_x = 0
        self.dir_y = 0
        return BehaviorTree.SUCCESS

    def set_random_target_boss(self):
        FIVE_METERS = int(PIXEL_PER_METER * 5)
        MAX_ATTEMPTS = 30

        for _ in range(MAX_ATTEMPTS):
            offset_x = random.randint(-FIVE_METERS, FIVE_METERS)
            offset_y = random.randint(-FIVE_METERS, FIVE_METERS)

            candidate_x = self.x + offset_x
            candidate_y = self.y + offset_y

            if is_valid_position(candidate_x, candidate_y, margin_meters=1):
                self.random_target_x = candidate_x
                self.random_target_y = candidate_y
                return BehaviorTree.SUCCESS

        self.random_target_x = self.x
        self.random_target_y = self.y
        return BehaviorTree.SUCCESS

    def move_to_random_position_boss(self):
        self.state = 'walk'

        dx = self.random_target_x - self.x
        dy = self.random_target_y - self.y
        dist = math.hypot(dx, dy)

        if dist > 20:
            nx = dx / dist
            ny = dy / dist
            self.dir_x = nx
            self.dir_y = ny

            new_x = self.x + self.dir_x * RUN_SPEED_PPS * self.speed_factor * game_framework.frame_time
            new_y = self.y + self.dir_y * RUN_SPEED_PPS * self.speed_factor * game_framework.frame_time

            if is_valid_position(new_x, new_y, margin_meters=1):
                self.x = new_x
                self.y = new_y
            else:
                return BehaviorTree.SUCCESS

            if self.dir_x > 0:
                self.face_dir = 1
            elif self.dir_x < 0:
                self.face_dir = -1

            return BehaviorTree.RUNNING
        else:
            self.dir_x = 0
            self.dir_y = 0
            self.state = 'idle'
            return BehaviorTree.SUCCESS

    def shoot_bombs_8_directions(self):
        cx, cy = self.get_center_pos()

        directions = [
            (1, 0),   # 동
            (1, 1),   # 북동
            (0, 1),   # 북
            (-1, 1),  # 북서
            (-1, 0),  # 서
            (-1, -1), # 남서
            (0, -1),  # 남
            (1, -1)   # 남동
        ]

        for dx, dy in directions:
            target_x = cx + dx * 1000
            target_y = cy + dy * 1000
            bomb = Bomb(cx, cy, target_x, target_y, damage=15)
            game_world.add_object(bomb, 1)
            game_world.add_collision_pair('bullet:player', bomb, None)

    def build_behavior_tree(self):
        attack_node = Sequence('공격',Condition('공격 범위 안?', self.is_attack_range),Action('공격 실행', self.do_attack))

        chase_node = Sequence('추적',Condition('감지 범위 안?', self.is_detection_range),Action('타겟으로 이동', self.move_to_target_boss))

        wander_node = Sequence('랜덤 배회',Action('랜덤 위치 설정', self.set_random_target_boss),Action('랜덤 위치로 이동', self.move_to_random_position_boss))

        root = Selector('보스 AI',attack_node,chase_node,wander_node)

        return BehaviorTree(root)

    def update(self):
        if not self.alive:
            return

        max_frames = self.sprite_info[self.state]['frames']

        if self.state == 'attack':
            self.frame = self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * self.frame_speed

            if self.frame >= max_frames:
                self.frame = max_frames - 1
                if not self.attack_finished:
                    self.attack_finished = True
                    self.post_attack_cooldown = self.attack_cooldown
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * self.frame_speed) % max_frames

        if self.post_attack_cooldown > 0:
            self.post_attack_cooldown -= game_framework.frame_time

        # bomb 발사 중일 때 타이머 관리
        if self.is_shooting_bomb:
            self.bomb_shoot_timer += game_framework.frame_time
            self.state = 'idle'
            self.dir_x = 0
            self.dir_y = 0

            if self.bomb_shoot_timer >= self.bomb_shoot_delay:
                self.is_shooting_bomb = False
                self.bomb_shoot_timer = 0

        # bomb 발사 체크
        if self.target and not self.is_shooting_bomb:
            cx, cy = self.get_center_pos()
            dx = self.target.x - cx
            dy = self.target.y - cy
            dist = math.hypot(dx, dy)

            if dist > PIXEL_PER_METER * 3:
                self.bomb_timer += game_framework.frame_time
                if self.bomb_timer >= self.bomb_cooldown:
                    self.is_shooting_bomb = True
                    self.state = 'idle'
                    self.dir_x = 0
                    self.dir_y = 0
                    self.shoot_bombs_8_directions()
                    self.bomb_timer = 0
                    self.bomb_shoot_timer = 0
            else:
                self.bomb_timer = 0

        # bomb 발사 중이 아닐 때만 BehaviorTree 실행
        if self.bt and not self.is_shooting_bomb:
            self.bt.run()

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

                cx, cy = self.get_center_pos()
                bx, by = cam.to_camera(cx, cy)
                draw_circle(int(bx), int(by), int(PIXEL_PER_METER * 3), 255, 255, 0)
                draw_circle(int(bx), int(by), int(PIXEL_PER_METER * 7), 0, 255, 0)
            else:
                draw_rectangle(*self.get_bb())
                draw_rectangle(*self.get_hit_bb())

                cx, cy = self.get_center_pos()
                draw_circle(int(cx), int(cy), int(PIXEL_PER_METER * 3), 255, 255, 0)
                draw_circle(int(cx), int(cy), int(PIXEL_PER_METER * 7), 0, 255, 0)

    def get_bb(self):
        if self.state == 'attack' and 8 <= int(self.frame) <= 11:
            offset = self.face_dir * 80
            return self.x - self.size + offset + 50, self.y - self.size - 50, self.x + self.size + offset - 50, self.y + self.size - 50
        else:
            return self.x, self.y, self.x, self.y

    def get_hit_bb(self):
        return self.x - 60, self.y - 150, self.x + 60, self.y + 20