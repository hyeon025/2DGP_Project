from pico2d import *
import time

import game_world
from job import Player_job, current_job, Job
import map as game_map
from player import Player
from particle import Particle , job_selec_atf
import game_framework
from camera import Camera

camera = Camera(world_w=5000, world_h=5000, screen_w=1200, screen_h=900)

def init():
    global world, player
    global job_selec_atf

    game_world.camera = camera

    map_obj = game_map.Game_Map(game_map.Map[game_map.current_map])
    game_world.add_object(map_obj,0)

    job = Job()
    game_world.add_object(job,2)

    player = Player(Player_job[current_job])
    game_world.add_object(player,3)

    for x,y in [(300,340),(600,340),(900,340),(600,680)]:
        particles = Particle(x,y)
        game_world.add_object(particles,2)
        game_world.add_collision_pair('particle:player',particles,player)



def handle_events():
    global Play
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_y:
            game_framework.show_bb = not game_framework.show_bb
        else:
            player.handle_event(event)

def update():
    player.update()
    if game_map.current_map != "Lobby":
        camera.update(player.x, player.y)

    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
    pass

def finish():
    game_world.clear()
    pass


def pause(): pass
def resume(): pass