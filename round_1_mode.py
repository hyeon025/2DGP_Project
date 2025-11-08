from pico2d import *
import game_world
import game_framework
import map as game_map
from job import Player_job, current_job, Job
from player import Player
from camera import Camera

camera = Camera(world_w=5000 * 2, world_h=5000 * 2, screen_w=1200, screen_h=900)


def init():
    global player, map_obj
    game_world.camera = camera

    map_obj = game_map.Game_Map(game_map.Map[game_map.current_map])
    game_world.add_object(map_obj, 0)

    player =Player(Player_job[current_job])
    player.x = 970 * 2
    player.y = 2560 * 2

    player.keys = {'d': False, 'a': False, 'w': False, 's': False}
    player.state_machine.current_state = player.IDLE
    player.IDLE.enter(('STOP', 0))

    game_world.add_object(player, 3)

    camera.update(player.x, player.y)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_y:
            game_framework.show_bb = not game_framework.show_bb
        else:
            if 'player' in globals():
                player.handle_event(event)

def update():
    game_world.update()

    if 'player' in globals():
        camera.update(player.x, player.y)

    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()
    game_world.camera = None
    globals().pop('player', None)
    globals().pop('map_obj', None)

def pause(): pass
def resume(): pass