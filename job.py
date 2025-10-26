import time

from pico2d import load_image

Player_job = {"alchemist": "asset/Character/alchemist_0.png", "assassin": "asset/Character/assassin_0.png", "shooter": "asset/Character/Shooter_0.png"}
current_job = "alchemist"

def Selectjob(player):
    global current_job
    for x, y in [(300, 340), (600, 340), (900, 340)]:
        dx = abs(player.x - x)
        dy = abs(player.y - y)
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < 50:
            if x == 300:
                current_job = "alchemist"
            elif x == 600:
                current_job = "assassin"
            elif x == 900:
                current_job = "officer"

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
