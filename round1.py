import random

from pico2d import load_image, delay
from PIL import Image
import game_framework
import game_world
from monster import Monster, AngryEggMonster, EggMonster, Boss1
from hp import BossHPBar

_background_cache = {}

rooms = {
    1: {'type': 1, 'num': 10, 'entered': False},
    2: {'type': 1, 'num': 14, 'entered': False},
    3: {'type': 3, 'num': 0, 'entered': False},
    4: {'type': 2, 'num': 1, 'entered': False},
}

_collision_data = None
_collision_width = 0
_collision_height = 0
_image_mode = None
current_collision_map = 'asset/Map/round1_collision.png'
current_background = 'asset/Map/round1_map.png'
current_room = None
monsters = []

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


def preload_backgrounds():
    global _background_cache
    bg_paths = [
        'asset/Map/round1_map.png',
        'asset/Map/round1_close_map.png',
        'asset/Map/round1_collision.png',
        'asset/Map/round1_close_collision.png',
    ]

    for path in bg_paths:
        if path not in _background_cache:
            _background_cache[path] = load_image(path)

def load_collision_map(map_path):
    global _collision_data, _collision_width, _collision_height, _image_mode, current_collision_map

    current_collision_map = map_path
    img = Image.open(map_path)
    _collision_data = img.load()
    _collision_width = img.width
    _collision_height = img.height
    _image_mode = img.mode


def spawn_monsters(room_num, player):
    global monsters

    for monster in monsters:
        game_world.remove_object(monster)
    monsters.clear()
    # print(f"Cleared all previous monsters")

    if rooms[room_num]['type'] == 0 or rooms[room_num]['num'] == 0:
        return

    monster_count = rooms[room_num]['num']
    monster_type = rooms[room_num]['type']

    if room_num == 1:
        current_monster_counts = {1: 4, 2: 6}
        base_x = 1960 * 2
        base_y = 2450 * 2

    elif room_num == 2:
        current_monster_counts = {1: 10, 2: 4}
        base_x = 1960 * 2
        base_y = 3140 * 2

    elif room_num == 4:
        # print(f"Boss1 spawning at room 4")
        base_x = player.x + 150
        base_y = player.y

        boss = Boss1(base_x, base_y, player)
        # print(f"Boss1 created at ({base_x}, {base_y}), Player at ({player.x}, {player.y})")
        monsters.append(boss)
        game_world.add_object(boss, 3)
        game_world.add_collision_pair('player:monster', player, boss)

        boss_hp_bar = BossHPBar(boss)
        game_world.add_object(boss_hp_bar, 4)

        if player.weapon:
            game_world.add_collision_pair('weapon:monster', player.weapon, boss)

        if player.skill:
            game_world.add_collision_pair('skill:monster', player.skill, boss)

        # print(f"Boss1 스폰. Total monsters: {len(monsters)}")
        return

    for monster_type, count in current_monster_counts.items():
        for i in range(count):
            spawn_x = base_x + random.randint(-100, 400)
            spawn_y = base_y + random.randint(-100, 400)

            if monster_type == 1:
                monster = EggMonster(spawn_x, spawn_y, player)
            elif monster_type == 2:
                monster = AngryEggMonster(spawn_x, spawn_y, player)
            else:
                continue

            monsters.append(monster)
            game_world.add_object(monster, 3)
            game_world.add_collision_pair('player:monster', player, monster)

            if player.weapon:
                game_world.add_collision_pair('weapon:monster', player.weapon, monster)

            if player.skill:
                game_world.add_collision_pair('skill:monster', player.skill, monster)

def change_map(background_path, collision_path, room_num, player):
    global current_background, current_room

    current_background = background_path
    current_room = room_num
    load_collision_map(collision_path)

    if background_path not in _background_cache:
        _background_cache[background_path] = load_image(background_path)

    bg_img = _background_cache[background_path]

    for obj in game_world.world[0]:
        if hasattr(obj, 'background'):
            obj.background = bg_img


    # spawn_monsters(room_num, player)


def round1Collision(player):
    global _collision_data, _collision_width, _collision_height, _image_mode

    if _collision_data is None:
        img = Image.open('asset/Map/round1_collision.png')
        _collision_data = img.load()
        _collision_width = img.width
        _collision_height = img.height
        _image_mode = img.mode

    dx = player.dir_x * RUN_SPEED_PPS * game_framework.frame_time * 1.2
    dy = player.dir_y * RUN_SPEED_PPS * game_framework.frame_time * 1.2

    next_x = player.x + dx
    next_y = player.y + dy

    scale = 10000.0 / _collision_width

    check_points = [
        (next_x, next_y),  # 중심
        (next_x - 40, next_y - 55),  # 좌하단
        (next_x + 40, next_y - 55),  # 우하단
        (next_x - 40, next_y),  # 좌상단
        (next_x + 40, next_y),  # 우상단
    ]

    can_move = True

    for px, py in check_points:
        img_x = int(px / scale)
        img_y = int(py / scale)

        if img_x < 0 or img_x >= _collision_width or img_y < 0 or img_y >= _collision_height:
            can_move = False
            return

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
            return

    if can_move:
        player.x = next_x
        player.y = next_y

        img_x = int(player.x / scale)
        img_y = int(player.y / scale)

        if 0 <= img_x < _collision_width and 0 <= img_y < _collision_height:
            pil_y = _collision_height - 1 - img_y
            pixel = _collision_data[img_x, pil_y]

            if _image_mode == 'RGB':
                r, g, b = pixel
            elif _image_mode == 'RGBA':
                r, g, b, a = pixel
            else:
                r = g = b = pixel if isinstance(pixel, int) else pixel[0]

            if r == 63 and g == 92 and b == 135:
                # 2번방 입장
                if not rooms[2]['entered']:
                    rooms[2]['entered'] = True
                    if rooms[2]['num'] > 0:
                        change_map('asset/Map/round1_close_map.png',
                                   'asset/Map/round1_close_collision.png', 2, player)
                        spawn_monsters(2, player)
                    else:
                        change_map('asset/Map/round1_map.png',
                                   'asset/Map/round1_collision.png', 2, player)

            elif r == 255 and g == 0 and b == 0:
                # 1번방 입장
                if not rooms[1]['entered']:
                    rooms[1]['entered'] = True
                    if rooms[1]['num'] > 0:
                        change_map('asset/Map/round1_close_map.png',
                                   'asset/Map/round1_close_collision.png', 1, player)
                        spawn_monsters(1, player)
                    else:
                        change_map('asset/Map/round1_map.png',
                                   'asset/Map/round1_collision.png', 1, player)

            elif r == 0 and g == 0 and b == 255:
                #4번방 입장
                print(f"Blue pixel detected - Room 4 entrance")
                if not rooms[4]['entered']:
                    print(f"Room 4 first entry")
                    rooms[4]['entered'] = True
                    if rooms[4]['num'] > 0:
                        print(f"Room 4 has monsters, closing map")
                        change_map('asset/Map/round1_close_map.png',
                                   'asset/Map/round1_close_collision.png', 4, player)
                        spawn_monsters(4, player)
                    else:
                        print(f"Room 4 has no monsters")
                        change_map('asset/Map/round1_map.png',
                               'asset/Map/round1_collision.png', 4, player)





