from pico2d import load_image , get_time, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_d, SDL_KEYUP, SDLK_a, SDLK_w, SDLK_s, SDLK_SPACE

from lobby import lobbyCollision
from map import current_map
from state_machine import StateMachine
import game_framework
import game_world
from job import Player_job
import job
import map as game_map
import round_1_mode


def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d
def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d
def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a
def w_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w
def w_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w
def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s
def s_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Walk:
    def __init__(self, player):
        self.player = player
        self.frame_time = 0

    def enter(self, e):
        if e[0] == 'INPUT':
            if space_down(e):
                self.handle_space(e)
                return
        self.update_key_and_dir(e)

    def handle_space(self, e):
        self.player.try_change_job()

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        self.player.x += self.player.dir_x * RUN_SPEED_PPS * game_framework.frame_time
        self.player.y += self.player.dir_y * RUN_SPEED_PPS * game_framework.frame_time
        if current_map == "Lobby":
            lobbyCollision(self.player)

        if not any(self.player.keys.values()) or (self.player.dir_x == 0 and self.player.dir_y == 0):
            self.player.state_machine.current_state = self.player.IDLE
            self.player.IDLE.enter(('STOP', 0))

    def draw(self):
        if self.player.face_dir == 1:
            self.player.job.clip_draw(int(self.player.frame) * 40, 40, 40, 40, self.player.x, self.player.y, 80, 80)
        else:
            self.player.job.clip_composite_draw(int(self.player.frame) * 40, 40, 40, 40, 0,'h', self.player.x, self.player.y, 80, 80)

    def update_key_and_dir(self, e):
        # 키 상태 업데이트
        if d_down(e):
            self.player.keys['d'] = True
        elif d_up(e):
            self.player.keys['d'] = False
        elif a_down(e):
            self.player.keys['a'] = True
        elif a_up(e):
            self.player.keys['a'] = False
        elif w_down(e):
            self.player.keys['w'] = True
        elif w_up(e):
            self.player.keys['w'] = False
        elif s_down(e):
            self.player.keys['s'] = True
        elif s_up(e):
            self.player.keys['s'] = False

        self.player.dir_x = 0
        self.player.dir_y = 0

        if self.player.keys['d']:
            self.player.dir_x += 1
        if self.player.keys['a']:
            self.player.dir_x -= 1
        if self.player.keys['w']:
            self.player.dir_y += 1
        if self.player.keys['s']:
            self.player.dir_y -= 1

        if self.player.dir_x > 0:
            self.player.face_dir = 1
        elif self.player.dir_x < 0:
            self.player.face_dir = -1


class Idle:
    def __init__(self, player):
        self.player = player
        self.frame_time = 0

    def enter(self, e):
        if e[0] == 'INPUT':
            if space_down(e):
                self.handle_space(e)
                return
            if d_up(e) or a_up(e) or w_up(e) or s_up(e):
                self.update_key_and_dir(e)
                return
        self.player.dir_x = 0
        self.player.dir_y = 0

    def handle_space(self, e):
        self.player.try_change_job()

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    def draw(self):
        if self.player.face_dir == 1:
            self.player.job.clip_draw(int(self.player.frame) * 40, 40, 40, 40,self.player.x, self.player.y, 80, 80)
        else:
            self.player.job.clip_composite_draw(int(self.player.frame) * 40, 40, 40, 40,0, 'h', self.player.x, self.player.y, 80, 80)

    def update_key_and_dir(self, e):
        if d_up(e):
            self.player.keys['d'] = False
        elif a_up(e):
            self.player.keys['a'] = False
        elif w_up(e):
            self.player.keys['w'] = False
        elif s_up(e):
            self.player.keys['s'] = False

        self.player.dir_x = 0
        self.player.dir_y = 0

        #키 상태 체크
        if self.player.keys['d']:
            self.player.dir_x += 1
        if self.player.keys['a']:
            self.player.dir_x -= 1
        if self.player.keys['w']:
            self.player.dir_y += 1
        if self.player.keys['s']:
            self.player.dir_y -= 1

        if self.player.dir_x != 0 or self.player.dir_y != 0:
            self.player.state_machine.current_state = self.player.WALK
            self.player.WALK.enter(e)

class Player:
    def __init__(self, job):
        self.x = 600
        self.y = 300
        self.job = load_image(job)
        self.face_dir = 1
        self.dir_x = 0
        self.dir_y = 0
        self.frame = 0
        self.colliding_particle = None

        self.keys = {'d': False, 'a': False, 'w': False, 's': False}

        self.IDLE = Idle(self)
        self.WALK = Walk(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {d_down: self.WALK,a_down: self.WALK,w_down: self.WALK,s_down: self.WALK,
                            d_up: self.WALK, a_up: self.WALK,w_up: self.WALK, s_up: self.WALK
                            ,space_down:  self.IDLE},
                self.WALK: {d_down: self.WALK, d_up: self.WALK,a_down: self.WALK, a_up: self.WALK,
                            w_down: self.WALK, w_up: self.WALK,s_down: self.WALK, s_up: self.WALK,
                            space_down: self.WALK}
            })

    def draw(self):
        self.state_machine.draw()
        if game_framework.show_bb:
            draw_rectangle(*self.get_bb())

    def update(self):
        self.state_machine.update()

    def handle_event(self,event):
        self.state_machine.handle_state_events(('INPUT', event))

    def change_job(self, new_job):
        self.job = load_image(new_job)

    def get_bb(self):
        return self.x - 30, self.y - 40, self.x + 30, self.y + 20

    def handle_collision(self, group, other):
        if group == 'particle:player':
            self.colliding_particle = other


    def try_change_job(self):
        if current_map != "Lobby" or not self.colliding_particle:
            return

        if not game_world.collide(self, self.colliding_particle):
            self.colliding_particle = None
            return

        if current_map == "Lobby" and self.colliding_particle:
            px = self.colliding_particle.x
            py = self.colliding_particle.y

            # 라운드 시작 파티클
            if px == 600 and py == 680:
                print("1라운드 시작!")
                game_map.current_map = "Round_1"
                game_framework.change_mode(round_1_mode)
                return

            # 직업 선택 파티클
            if py == 340:
                job_positions = {
                    300: "alchemist",
                    600: "assassin",
                    900: "officer"
                }

                if px in job_positions:
                    job_name = job_positions[px]
                    job.current_job = job_name
                    if job_name in Player_job:
                        self.change_job(Player_job[job_name])
                        print(f"직업 변경: {job_name}")