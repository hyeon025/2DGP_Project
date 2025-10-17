from pico2d import load_image


class Player:
    def __init__(self, job):
        self.x = 600
        self.y = 300
        self.job = load_image(job)

    def draw(self):
        self.job.clip_draw(0, 80, 40, 40, self.x, self.y, 80, 80)

    def update(self):
        pass

    def handle_events(self):
        pass