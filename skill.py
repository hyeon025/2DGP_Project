from pico2d import load_image, draw_rectangle
import game_framework
import game_world
import math


class Skill:
    def __init__(self):
        self.cooldown = 5.0
        self.cooldown_timer = 0
        self.is_active = False
        self.duration = 0
        self.duration_timer = 0

    def use(self):
        if self.cooldown_timer <= 0:
            self.is_active = True
            self.cooldown_timer = self.cooldown
            self.duration_timer = self.duration
            self.on_use()
            return True
        else:
            print(f"쿨타임 남음: {self.cooldown_timer:.1f}초")
            return False

    def on_use(self):
        pass

    def update(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= game_framework.frame_time

        if self.is_active:
            self.duration_timer -= game_framework.frame_time
            self.on_update()

            if self.duration_timer <= 0:
                self.is_active = False
                self.on_end()

    def on_update(self):
        pass

    def on_end(self):
        print(f"{self.__class__.__name__} 종료")

    def draw(self):
        pass

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass

