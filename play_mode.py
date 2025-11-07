from pico2d import *
import time
from job import Player_job, current_job, Job
from map import Game_Map, Map, current_map
from player import Player
from particle import Particle , job_selec_atf
import game_framework



def init():
    global world, player
    global job_selec_atf

    world = []
    map = Game_Map(Map[current_map])
    world.append(map)
    job = Job()
    world.append(job)
    for x,y in [(300,340),(600,340),(900,340),(600,680)]:
        particles = Particle(x,y)
        world.append(particles)
    player = Player(Player_job[current_job])
    world.append(player)
    pass


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
    for o in world:
        o.update()


def draw():
    clear_canvas()
    for game_object in world:
        game_object.draw()
    update_canvas()
    pass

def finish():
    world.clear()
    pass


def pause(): pass
def resume(): pass