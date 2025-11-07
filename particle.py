from pico2d import load_image
from map import current_map

job_selec_atf = [(300,340),(600,340),(900,340),(600,680)]

class Particle:
    def __init__(self):
        self.image = load_image('asset/Particle/atf_star.png')

    def draw(self):
        if current_map == "Lobby":
            for x,y in job_selec_atf:
                self.image.draw(x, y, 40, 40)

    def update(self):
        pass

    def get_bb(self):
        return self.x-10, self.y-10, self.x+10, self.y+10