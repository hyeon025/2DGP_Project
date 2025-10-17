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
        pass

    def draw(self):
        self.player.job.clip_draw(0, 80, 40, 40, self.player.x, self.player.y, 80, 80)

class Player:
    def __init__(self, job):
        self.x = 600
        self.y = 300
        self.job = load_image(job)

        self.IDLE = Idle(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
            self.IDLE:{}
            })


    def draw(self):
        self.state_machine.draw()

    def update(self):
        pass

    def handle_events(self):
        pass