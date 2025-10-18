from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_d, SDL_KEYUP, SDLK_a, SDLK_w, SDLK_s
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

class Walk_xy:
    def __init__(self, player):
        self.player = player

    def enter(self,e):
        if d_down(e):
            self.player.dir_x += 1
            self.player.face_dir = 1
        elif d_up(e):
            self.player.dir_x -= 1
        elif a_down(e):
            self.player.dir_x -= 1
            self.player.face_dir = -1
        elif a_up(e):
            self.player.dir_x += 1
        elif w_down(e):
            self.player.dir_y += 1
        elif w_up(e):
            self.player.dir_y -= 1
        elif s_down(e):
            self.player.dir_y -= 1
        elif s_up(e):
            self.player.dir_y += 1

    def exit(self,e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 8
        self.player.x += self.player.dir_x * 0.5
        self.player.y += self.player.dir_y * 0.5

    def draw(self):
        if self.player.face_dir == 1:
            self.player.job.clip_draw(self.player.frame * 40, 40, 40, 40, self.player.x, self.player.y, 80, 80)
        else:
            self.player.job.clip_composite_draw(self.player.frame * 40, 40, 40, 40, 0,'h', self.player.x, self.player.y, 80, 80)


class Walk_y:
    def __init__(self, player):
        self.player = player

    def enter(self,e):
        if w_down(e):
            self.player.dir_y += 1
        elif w_up(e):
            self.player.dir_y -= 1
        elif s_down(e):
            self.player.dir_y -= 1
        elif s_up(e):
            self.player.dir_y += 1

    def exit(self,e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 8
        self.player.y += self.player.dir_y * 0.5

    def draw(self):
        if self.player.face_dir == 1:
            self.player.job.clip_draw(self.player.frame * 40, 40, 40, 40, self.player.x, self.player.y, 80, 80)
        else:
            self.player.job.clip_composite_draw(self.player.frame * 40, 40, 40, 40, 0,'h', self.player.x, self.player.y, 80, 80)


class Walk_x:
    def __init__(self, player):
        self.player = player

    def enter(self,e):
        if d_down(e):
            self.player.dir_x += 1
            self.player.face_dir = 1
        elif d_up(e):
            self.player.dir_x -= 1
        elif a_down(e):
            self.player.dir_x -= 1
            self.player.face_dir = -1
        elif a_up(e):
            self.player.dir_x += 1

    def exit(self,e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 8
        self.player.x += self.player.dir_x * 0.5

    def draw(self):
        if self.player.face_dir == 1:
            self.player.job.clip_draw(self.player.frame * 40, 40, 40, 40, self.player.x, self.player.y, 80, 80)
        else:
            self.player.job.clip_composite_draw(self.player.frame * 40, 40, 40, 40, 0,'h', self.player.x, self.player.y, 80, 80)

class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self,e):
        self.player.dir_x = 0
        self.player.dir_y = 0

    def exit(self,e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 8

    def draw(self):
        if self.player.face_dir == 1:
            self.player.job.clip_draw(self.player.frame * 40, 80, 40, 40, self.player.x, self.player.y, 80, 80)
        else:
            self.player.job.clip_composite_draw(self.player.frame * 40, 80, 40, 40, 0,'h', self.player.x, self.player.y, 80, 80)

class Player:
    def __init__(self, job):
        self.x = 600
        self.y = 300
        self.job = load_image(job)
        self.face_dir = 1
        self.dir_x = 0
        self.dir_y = 0
        self.frame = 0

        self.IDLE = Idle(self)
        self.WALK_X = Walk_x(self)
        self.WALK_Y = Walk_y(self)
        self.WALK_XY = Walk_xy(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
            self.IDLE:{d_down: self.WALK_X, a_down: self.WALK_X, w_down: self.WALK_Y, s_down: self.WALK_Y
                       , d_up:  self.WALK_X, a_up:  self.WALK_X, w_up:  self.WALK_Y, s_up: self.WALK_Y},
            self.WALK_X:{d_up: self.IDLE, a_up: self.IDLE, w_up: self.WALK_XY, s_up: self.WALK_XY,
                        d_down: self.IDLE, a_down: self.IDLE, w_down: self.WALK_XY, s_down: self.WALK_XY},
            self.WALK_Y:{w_up: self.IDLE, s_up: self.IDLE, d_up: self.WALK_XY, a_up: self.WALK_XY,
                         w_down: self.IDLE, s_down: self.IDLE, d_down: self.WALK_XY,a_down: self.WALK_XY},
            self.WALK_XY:{d_up: self.WALK_Y, a_up: self.WALK_Y, w_up: self.WALK_X, s_up: self.WALK_X,
                          d_down: self.WALK_Y, a_down: self.WALK_Y, w_down: self.WALK_X, s_down: self.WALK_X}
            })


    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()

    def handle_event(self,event):
        self.state_machine.handle_state_events(('INPUT', event))