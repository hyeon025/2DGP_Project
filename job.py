import time

from pico2d import load_image

Player_job = {"alchemist": "asset/Character/alchemist_0.png", "assassin": "asset/Character/assassin_0.png", "officer": "asset/Character/officer_0.png"}
current_job = "alchemist"

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def Selectjob(player):
    global current_job
    for x, y in [(300, 340), (600, 340), (900, 340)]:
        dx = abs(player.x - x)
        dy = abs(player.y - y)
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < 30:
            if x == 300:
                current_job = "alchemist"
            elif x == 600:
                current_job = "assassin"
            elif x == 900:
                current_job = "officer"
            if current_job in Player_job:
                player.change_job(Player_job[current_job])
                print(f"직업 변경: {current_job}")

class Job:
    def __init__(self):
        self.alchemist = load_image('asset/Character/alchemist_0.png')
        self.assassin = load_image('asset/Character/assassin_0.png')
        self.officer = load_image('asset/Character/officer_0.png')
        self.frame = 0
        self.frame_time = time.time()

    def draw(self):
        self.alchemist.clip_draw(self.frame * 40,80,40,40,300,400,80,80)
        self.assassin.clip_draw(self.frame * 40,80,40,40,600,400,80,80)
        self.officer.clip_draw(self.frame * 40,80,40,40,900,400,80,80)

    def update(self):
        self.frame_time += 0.016
        if self.frame_time > 0.5:
            self.frame = (self.frame + 1) % 8
            self.frame_time = 0
