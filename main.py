from pico2d import *

from job import Player_job, current_job
from map import Game_Map, Map, current_map
from player import Player


def reset_canvas():
    global world, player

    world = []
    map = Game_Map(Map[current_map])

    world.append(map)
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