import time

from pico2d import load_image, load_font
import map as game_map

Player_job = {"alchemist": "asset/Character/alchemist_0.png", "assassin": "asset/Character/assassin_0.png", "officer": "asset/Character/officer_0.png"}
current_job = "alchemist"
job_cleared = {"alchemist": False, "assassin": False, "officer": False}
using_skill2 = {"alchemist": False, "assassin": False, "officer": False}

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
    font = None

    def __init__(self):
        if JobUI.images is None:
            JobUI.images = {
                'alchemist': {
                    '1': load_image('asset/UI/alchemist_1.png'),
                    '2': load_image('asset/UI/alchemist_2.png'),
                    '2_closed': load_image('asset/UI/close_alchemist_2.png')
                },
                'assassin': {
                    '1': load_image('asset/UI/assassin_1.png'),
                    '2': load_image('asset/UI/assassin_2.png'),
                    '2_closed': load_image('asset/UI/close_assassin_2.png')
                },
                'officer': {
                    '1': load_image('asset/UI/officer_1.png'),
                    '2': load_image('asset/UI/officer_2.png'),
                    '2_closed': load_image('asset/UI/close_officer_2.png')
                }
            }
        if JobUI.font is None:
            JobUI.font = load_font('ENCR10B.TTF', 20)

    def update(self):
        pass

    def draw(self):
        if game_map.current_map != "Lobby":
            return

        job_images = JobUI.images.get(current_job, JobUI.images['alchemist'])


        job_images['1'].draw(50, 500, 40, 40)
        JobUI.font.draw(65, 485, '1', (255, 255, 255))

        if job_cleared[current_job]:
            job_images['2'].draw(50, 450, 40, 40)
        else:
            job_images['2_closed'].draw(50, 450, 40, 40)
        JobUI.font.draw(65, 435, '2', (255, 255, 255))
