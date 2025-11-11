from pico2d import *

import game_framework
import play_mode
import round1

image = None
logo_start_time = 0


def init():
    global image,logo_start_time

    image = load_image('logo/tuk_credit.png')
    logo_start_time = get_time()


def update():
    if get_time() - logo_start_time > 1:
        round1.preload_backgrounds()
        game_framework.change_mode(play_mode)

def draw():
    clear_canvas()
    image.draw(600, 450, 1200, 900)
    update_canvas()
    pass

def finish():
    global image
    del image

    pass

def handle_events():
    event_list = get_events()


def pause(): pass
def resume(): pass