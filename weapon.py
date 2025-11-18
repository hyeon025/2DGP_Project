from pico2d import load_image, draw_rectangle
import game_framework
import game_world
import math

import round1


class Weapon:
    image = None

    def __init__(self, own, damage=10, attack_duration=0.3, cooldown=0.5):
        if Weapon.image is None:
            Weapon.image = load_image('asset/Weapon/ice_sword_particle.png')
        self.own = own
        self.damage = damage
        self.cooldown = cooldown
        self.attack_duration = attack_duration
        self.is_attacking = False

        self.attack_timer = 0
        self.cooldown_timer = 0

        self.frame = 0

        self.attack_range = 30
        self.attack_width = 41 * 1.5
        self.attack_height = 55 * 1.5

    def attack(self):
        if self.cooldown_timer <= 0 and not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = self.attack_duration
            self.cooldown_timer = self.cooldown
            self.frame = 0
            print(f"공격, 데미지: {self.damage}")
        pass

    def update(self):
        if self.is_attacking:
            self.attack_timer -= game_framework.frame_time

            progress = 1.0 - (self.attack_timer / self.attack_duration)
            self.frame = int(progress * 5)

            if self.frame >= 5:
                self.frame = 5 - 1

            if self.attack_timer <= 0:
                self.is_attacking = False
                print("공격 완료")

        if self.cooldown_timer > 0:
            self.cooldown_timer -= game_framework.frame_time

    def draw(self):
        if not self.is_attacking:
            return

        cam = game_world.camera

        offset_x = self.attack_range * self.own.face_dir
        wx = self.own.x + offset_x + (15 * self.own.face_dir)
        wy = self.own.y - 25

        if cam:
            sx, sy = cam.to_camera(wx, wy)
        else:
            sx, sy = wx, wy

        if Weapon.image:
            if self.own.face_dir == 1:
                Weapon.image.clip_draw(self.frame * 41, 0, 41, 55, sx, sy, self.attack_width, self.attack_height)
            else:
                Weapon.image.clip_composite_draw(self.frame * 41, 0, 41, 55 ,0, 'h', sx, sy, self.attack_width, self.attack_height)
        if game_framework.show_bb:
            if cam:
                l, b, r, t = self.get_bb()
                sl, sb = cam.to_camera(l, b)
                sr, st = cam.to_camera(r, t)
                draw_rectangle(sl, sb, sr, st)
            else:
                draw_rectangle(*self.get_bb())

    def get_bb(self):
        if not self.is_attacking:
            return 0, 0, 0, 0

        offset_x = self.attack_range * self.own.face_dir
        wx = self.own.x + offset_x + (15 * self.own.face_dir)
        wy = self.own.y - 25

        half_w = self.attack_width // 2
        half_h = self.attack_height // 2

        return wx - half_w, wy - half_h, wx + half_w, wy + half_h

    def handle_collision(self, group, other):
        if group == 'weapon:monster' and self.is_attacking:
            if hasattr(other, 'hp'):
                other.hp -= self.damage
                print(f"몬스터 공격, 몬스터 남은 HP: {other.hp}")
                if other.hp <= 0:
                    other.alive = False
                    game_world.collision_pairs['weapon:monster'][1].remove(other)
                    round1.rooms[round1.current_room]['num'] -= 1

                    if round1.current_room == 1 and all(not m.alive for m in round1.monsters):
                        round1.change_map('asset/Map/round1_map.png', 'asset/Map/round1_collision.png', 1, self.own)

                    if round1.current_room == 2 and all(not m.alive for m in round1.monsters):
                        round1.change_map('asset/Map/round1_map.png', 'asset/Map/round1_collision.png', 2, self.own)

