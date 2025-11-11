from pico2d import load_image, draw_rectangle
import game_framework
import game_world

class Weapon:
    image = None

    def __init__(self, own, damage=10, attack_duration=0.3, cooldown=0.5):
        if Weapon.image is None:
            Weapon.image = load_image('asset/Weapon/ice_sword.png')
        self.own = own
        self.damage = damage
        self.attack_timer = 0
        self.cooldown_timer = 0

        self.attack_range = 100
        self.attack_width = 100
        self.attack_height = 100