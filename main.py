from pico2d import *

def reset_canvas():
    pass


def handle_events():
    pass

def update_map():
    pass


def render_world():
    pass

open_canvas()

reset_canvas()

Play = True

while Play:
    handle_events()

    update_map()

    render_world()

    delay(0.05)


close_canvas()