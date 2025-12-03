from pico2d import load_image , draw_rectangle
from map import current_map
import game_framework
import game_world

job_selec_atf = [(300,340),(600,340),(900,340),(600,680)]

class Particle:
    image = None

    def __init__(self,x,y):
        if Particle.image is None:
            Particle.image = load_image('asset/Particle/atf_star.png')
        self.image = Particle.image
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

class BossDeathParticle:
    image = None

    def __init__(self, x, y):
        if BossDeathParticle.image is None:
            BossDeathParticle.image = load_image('asset/Particle/atf_star.png')
        self.image = BossDeathParticle.image
        self.x = x
        self.y = y

    def draw(self):
        cam = game_world.camera
        if cam:
            sx, sy = cam.to_camera(self.x,self.y)
        else:
            sx, sy = self.x, self.y

        self.image.clip_draw(0,0,80,80,sx, sy, 40,40)

        if game_framework.show_bb:
            if cam:
                l, b, r, t = self.get_bb()
                sl, sb = cam.to_camera(l, b)
                sr, st = cam.to_camera(r, t)
                draw_rectangle(sl, sb, sr, st)
            else:
                draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def handle_collision(self, group, other):
        pass