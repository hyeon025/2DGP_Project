from pico2d import *

Player_job = {"alchemist":"asset/Character/alchemist_0.png","assassin":"asset/Character/assassin_0.png","shooter":"asset/Character/Shooter_0.png"}
current_job = "alchemist"

class Player:
    def __init__(self, job):
        self.x = 600
        self.y = 300
        self.job = load_image(job)

    def draw(self):
        self.job.clip_draw(0, 80, 40, 40, self.x, self.y, 80, 80)

def reset_canvas():
    global Play

    Play = True

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