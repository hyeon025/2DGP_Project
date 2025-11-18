from pico2d import load_image, draw_rectangle
import game_framework
import game_world
import math


class Skill:
    def __init__(self,owner):
        self.owner = owner
        self.cooldown = 5.0
        self.cooldown_timer = 0
        self.is_active = False
        self.duration = 0
        self.duration_timer = 0

    def use(self):
        if self.is_active:
            print("스킬이 이미 사용 중입니다.")
            return False
        if self.cooldown_timer > 0:
            print(f"쿨타임 남음: {self.cooldown_timer:.1f}초")
            return False
        self.is_active = True
        self.cooldown_timer = self.cooldown
        self.duration_timer = self.duration
        self.on_use()
        return True

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

class AlchemistSkill(Skill):
    image = None

    def __init__(self, owner):
        super().__init__(owner)
        if AlchemistSkill.image is None:
            AlchemistSkill.image = load_image('asset/Weapon/alchemist_1.png')

        self.cooldown = 0.5
        self.duration = 0.5
        self.damage = 40
        self.range = 250
        self.frame = 0
        self.throw_x = 0
        self.throw_y = 0
        self.target_x = 0
        self.target_y = 0
        self.skill_dir = 1
        self.explosion_timer = 0

    def on_use(self):
        self.start_x = self.owner.x
        self.start_y = self.owner.y
        self.skill_dir = self.owner.face_dir
        self.target_x = self.start_x + (self.range * self.skill_dir)
        self.target_y = self.start_y
        self.frame = 0
        self.explosion_timer = 0

    def on_update(self):
        progress = 1.0 - (self.duration_timer / self.duration)
        self.frame = int(progress * 5) % 6

        self.throw_x = self.start_x + (self.range * self.skill_dir * progress)
        self.throw_y = self.start_y + math.sin(progress * math.pi) * 50

    def on_end(self):
        self.explosion_timer = 0.5
        # game_world.remove_object(self)

    def update(self):
        super().update()
        if not self.is_active and self.explosion_timer > 0:
            self.explosion_timer -= game_framework.frame_time
            if self.explosion_timer <= 0:
                game_world.remove_object(self)

    def draw(self):

        cam = game_world.camera
        if cam:
            sx, sy = cam.to_camera(self.throw_x, self.throw_y)
            tx, ty = cam.to_camera(self.target_x, self.target_y)
        else:
            sx, sy = self.throw_x, self.throw_y
            tx, ty = self.target_x, self.target_y

        if self.is_active:
            if self.image:
                self.image.clip_draw(0, 0, 21, 21, sx, sy, 30, 30)

        if not self.is_active and self.explosion_timer > 0:
            if self.image:
                self.image.clip_draw(82, 0, 61, 61, tx, ty, 60, 60)

        if game_framework.show_bb:
            if cam:
                l, b, r, t = self.get_bb()
                sl, sb = cam.to_camera(l, b)
                sr, st = cam.to_camera(r, t)
                draw_rectangle(sl, sb, sr, st)
            else:
                draw_rectangle(*self.get_bb())

    def get_bb(self):
        if not self.is_active:
            return 0, 0, 0, 0
        return self.throw_x - 20, self.throw_y - 20, self.throw_x + 20, self.throw_y + 20

    def handle_collision(self, group, other):
        if group == 'skill:monster' and self.is_active:
            if hasattr(other, 'hp') and other.alive:
                other.hp -= self.damage
                print(f"피격 성공, 몬스터 HP: {other.hp}")
                if other.hp <= 0:
                    other.alive = False


class AssassinSkill(Skill):
    image = None

    def __init__(self, owner):
        super().__init__(owner)
        if AssassinSkill.image is None:
            AssassinSkill.image = load_image('asset/Weapon/assassin_1.png')

        self.cooldown = 0.2
        self.duration = 0.3
        self.dash_distance = 300
        self.dash_speed = 0
        self.start_x = 0
        self.start_y = 0
        self.target_x = 0
        self.target_y = 0

    def on_use(self):
        pass

    def on_update(self):
        pass

    def on_end(self):
        pass

    def draw(self):
        if not self.is_active:
            return

        cam = game_world.camera
        if cam:
            sx, sy = cam.to_camera(self.owner.x, self.owner.y)
        else:
            sx, sy = self.owner.x, self.owner.y


class OfficerSkill(Skill):
    image = None

    def __init__(self, owner):
        super().__init__(owner)
        if OfficerSkill.image is None:
            OfficerSkill.image = load_image('asset/Weapon/officer_1.png')

        self.cooldown = 8.0
        self.duration = 3.0
        self.heal_amount = 20
        self.buff_range = 150
        self.frame = 0
        self.center_x = 0
        self.center_y = 0

    def on_use(self):
        pass


    def on_update(self):
        pass

    def on_end(self):
        pass

    def draw(self):
        if not self.is_active:
            return

        cam = game_world.camera
        if cam:
            sx, sy = cam.to_camera(self.center_x, self.center_y)
        else:
            sx, sy = self.center_x, self.center_y

def create_skill(job_name,owner):
    skill_map = {
        'alchemist': AlchemistSkill,
        'assassin': AssassinSkill,
        'officer': OfficerSkill
    }
    skill_class = skill_map.get(job_name)
    if skill_class:
        return skill_class(owner)
    else:
        print(f"없는 직업: {job_name}")
        return None