from pico2d import *

from player import Player

Player_job = {"alchemist":"asset/Character/alchemist_0.png","assassin":"asset/Character/assassin_0.png","shooter":"asset/Character/Shooter_0.png"}
current_job = "alchemist"

def reset_canvas():
    global world, player

    world = []
    player = Player(Player_job[current_job])
    world.append(player)
    pass


def handle_events():
    global Play
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Play = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                Play = False
        else:
            player.handle_event(event)

def update_map():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for game_object in world:
        game_object.draw()
    update_canvas()
    pass

open_canvas(1200,900)

reset_canvas()

Play = True

while Play:
    handle_events()

    update_map()

    render_world()


close_canvas()