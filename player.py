from pico2d import load_image

from state_machine import StateMachine


class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self,e):
        self.player.dir = 0

    def exit(self,e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 8

    def draw(self):
        if self.player.face_dir == 1:
            self.player.job.clip_draw(self.player.frame * 40, 80, 40, 40, self.player.x, self.player.y, 80, 80)
        else:
            self.player.job.composite_draw(self.player.frame * 40, 80, 40, 40, 0,'h', self.player.x, self.player.y, 80, 80)

class Player:
    def __init__(self, job):
        self.x = 600
        self.y = 300
        self.job = load_image(job)
        self.face_dir = 1
        self.dir = 0
        self.frame = 0

        self.IDLE = Idle(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
            self.IDLE:{}
            })


    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()

    def handle_events(self):
        pass