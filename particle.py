from pico2d import load_image

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image('asset/Particle/atf_star.png')

    def draw(self):
        self.image.draw(self.x, self.y, 40, 40)
