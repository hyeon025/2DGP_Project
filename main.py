from pico2d import *

def reset_canvas():
    pass


def handle_events():
    global Play
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Play = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                Play = False


def update_map():
    pass


def render_world():
    clear_canvas()

    update_canvas()
    pass

open_canvas(1200,900)

reset_canvas()

Play = True

while Play:
    handle_events()

    update_map()

    render_world()

    delay(0.05)


close_canvas()