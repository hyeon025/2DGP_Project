from pico2d import load_image

Player_job = {"alchemist": "asset/Character/alchemist_0.png", "assassin": "asset/Character/assassin_0.png", "shooter": "asset/Character/Shooter_0.png"}
current_job = "alchemist"

class Job:
    def __init__(self):
        self.alchemist = load_image('asset/Character/alchemist_0.png')
        self.assassin = load_image('asset/Character/assassin_0.png')
        self.officer = load_image('asset/Character/officer_0.png')
        self.frame = 0
    def draw(self):
        self.alchemist.clip_draw(self.frame * 40,80,40,40,300,400,80,80)
        self.assassin.clip_draw(self.frame * 40,80,40,40,600,400,80,80)
        self.officer.clip_draw(self.frame * 40,80,40,40,900,400,80,80)