import time

from pico2d import load_image
import map as game_map

Player_job = {"alchemist": "asset/Character/alchemist_0.png", "assassin": "asset/Character/assassin_0.png", "officer": "asset/Character/officer_0.png"}
current_job = "alchemist"

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

class JobUI:
    images = None

    def __init__(self):
        if JobUI.images is None:
            JobUI.images = {
                'alchemist': [
                    load_image('asset/UI/alchemist_1.png'),
                    load_image('asset/UI/alchemist_2.png')
                ],
                'assassin': [
                    load_image('asset/UI/assassin_1.png'),
                    load_image('asset/UI/assassin_2.png')
                ],
                'officer': [
                    load_image('asset/UI/officer_1.png'),
                    load_image('asset/UI/officer_2.png')
                ]
            }

    def update(self):
        pass

    def draw(self):
        if game_map.current_map != "Lobby":
            return

        job_images = JobUI.images.get(current_job, JobUI.images['alchemist'])

        job_images[0].draw(50, 500, 40, 40)
        job_images[1].draw(50, 450, 40, 40)
