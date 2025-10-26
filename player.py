from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_d, SDL_KEYUP, SDLK_a, SDLK_w, SDLK_s, SDLK_SPACE

from lobby import lobbyCollision
from map import current_map
from state_machine import StateMachine


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

class Walk:
    def __init__(self, player):
        self.player = player
        self.frame_time = 0

    def enter(self, e):
        self.update_key_and_dir(e)

    def exit(self, e):
        pass

    def do(self):
        self.frame_time += 0.016
        if self.frame_time > 0.5:
            self.player.frame = (self.player.frame + 1) % 8
            self.frame_time = 0

        self.player.x += self.player.dir_x * 0.5
        self.player.y += self.player.dir_y * 0.5
        if current_map == "Lobby":
            lobbyCollision(self.player)

        if not any(self.player.keys.values()) or (self.player.dir_x == 0 and self.player.dir_y == 0):
            self.player.state_machine.current_state = self.player.IDLE
            self.player.IDLE.enter(('STOP', 0))

    def draw(self):
        if self.player.face_dir == 1:
            self.player.job.clip_draw(self.player.frame * 40, 40, 40, 40, self.player.x, self.player.y, 80, 80)
        else:
            self.player.job.clip_composite_draw(self.player.frame * 40, 40, 40, 40, 0,'h', self.player.x, self.player.y, 80, 80)

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
        if current_map == "Lobby":
            from job import Selectjob
            Selectjob(self.player)

    def exit(self, e):
        pass

    def do(self):
        self.frame_time += 0.016
        if self.frame_time > 0.5:
            self.player.frame = (self.player.frame + 1) % 8
            self.frame_time = 0

    def draw(self):
        if self.player.face_dir == 1:
            self.player.job.clip_draw(self.player.frame * 40, 80, 40, 40,self.player.x, self.player.y, 80, 80)
        else:
            self.player.job.clip_composite_draw(self.player.frame * 40, 80, 40, 40,0, 'h', self.player.x, self.player.y, 80, 80)

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

        self.keys = {'d': False, 'a': False, 'w': False, 's': False}

        self.IDLE = Idle(self)
        self.WALK = Walk(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {d_down: self.WALK,a_down: self.WALK,w_down: self.WALK,s_down: self.WALK,
                            d_up: self.WALK, a_up: self.WALK,w_up: self.WALK, s_up: self.WALK},
                self.WALK: {d_down: self.WALK, d_up: self.WALK,a_down: self.WALK, a_up: self.WALK,
                            w_down: self.WALK, w_up: self.WALK,s_down: self.WALK, s_up: self.WALK}
            })

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()

    def handle_event(self,event):
        self.state_machine.handle_state_events(('INPUT', event))
