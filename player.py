from pico2d import load_image


class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self):
        pass

    def exit(self):
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

    def draw(self):
        self.job.clip_draw(0, 80, 40, 40, self.x, self.y, 80, 80)

    def update(self):
        pass

    def handle_events(self):
        pass