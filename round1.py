from pico2d import load_image
from PIL import Image
import game_framework

_collision_data = None
_collision_width = 0
_collision_height = 0
_image_mode = None

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

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

    img_x = int(next_x / scale)
    img_y = int(next_y / scale)

    if img_x < 0 or img_x >= _collision_width or img_y < 0 or img_y >= _collision_height:
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

    # 검은색
    if r < 1 and g < 1 and b < 1:
        print('충돌!')
        return

    player.x = next_x
    player.y = next_y