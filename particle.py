from pico2d import load_image , draw_rectangle
from map import current_map
import game_framework

job_selec_atf = [(300,340),(600,340),(900,340),(600,680)]

class Particle:
    def __init__(self,x,y):
        self.image = load_image('asset/Particle/atf_star.png')
        self.x = x
        self.y = y

    def draw(self):
        if current_map == "Lobby":
            self.image.draw(self.x, self.y, 40, 40)
            if game_framework.show_bb:
                draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x-10, self.y-10, self.x+10, self.y+10

    def handle_collision(self, group, other):
        pass