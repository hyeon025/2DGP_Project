from pico2d import *

import game_framework
import play_mode

image = None
logo_start_time = 0


def init():
    global image,logo_start_time

    image = load_image('logo.tuk_credit.png')
    logo_start_time = get_time()


def update():
    if get_time() - logo_start_time > 2:
        game_framework.quit()

def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()
    pass

def finish():
    global image
    del image

    pass

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(play_mode)


def pause(): pass
def resume(): pass