from pico2d import load_image, draw_rectangle
import game_world
import game_framework
import random

class PlayerHPBar:
    hp_images = None
    frame_image = None

    def __init__(self, player):
        self.player = player

        if PlayerHPBar.hp_images is None:
            PlayerHPBar.hp_images = {}
            for i in range(0, 101, 10):
                img = load_image(f'asset/hp/player/{i}.png')
                PlayerHPBar.hp_images[i] = img

        if PlayerHPBar.frame_image is None:
            PlayerHPBar.frame_image = load_image('asset/hp/player/Frame.png')

    def update(self):
        pass

    def draw(self):
        # 플레이어의 현재 HP를 실시간으로 반영
        hp_value = max(0, min(200, self.player.hp))
        hp_percentage = int((hp_value / 200) * 100)
        hp_rounded = (hp_percentage // 10) * 10

        screen_x = 100
        screen_y = 800

        if hp_rounded in PlayerHPBar.hp_images:
            PlayerHPBar.hp_images[hp_rounded].clip_draw(0,0,100,100,screen_x, screen_y,300,300)

        PlayerHPBar.frame_image.clip_draw(0,0,100,100,screen_x, screen_y,300,300)

    def get_bb(self):
        return 0, 0, 0, 0

    def handle_collision(self, group, other):
        pass

class BossHPBar:
    images = None

    def __init__(self, boss):
        self.boss = boss
        self.max_hp = boss.hp

        if BossHPBar.images is None:
            BossHPBar.images = []
            for i in range(51):
                img = load_image(f'asset/hp/monster/{i}.png')
                BossHPBar.images.append(img)

    def update(self):
        pass

    def draw(self):
        if not self.boss.alive and self.boss.death_animation_finished:
            return

        cam = game_world.camera

        hp_ratio = max(0, min(1, self.boss.hp / self.max_hp))
        image_index = int((1 - hp_ratio) * 50)
        image_index = max(0, min(50, image_index))

        hp_bar_y = self.boss.y + 120

        if cam:
            sx, sy = cam.to_camera(self.boss.x, hp_bar_y)
        else:
            sx, sy = self.boss.x, hp_bar_y

        img = BossHPBar.images[image_index]
        img_w = img.w
        img_h = img.h

        scale = 262 / img_w
        display_h = img_h * scale

        img.draw(sx, sy, 262, display_h)

    def get_bb(self):
        return 0, 0, 0, 0

    def handle_collision(self, group, other):
        pass

class MonsterHPBar:
    images = None

    def __init__(self, monster):
        self.monster = monster
        self.max_hp = monster.hp

        if MonsterHPBar.images is None:
            MonsterHPBar.images = []
            for i in range(51):
                img = load_image(f'asset/hp/monster/{i}.png')
                MonsterHPBar.images.append(img)

    def update(self):
        if not self.monster.alive:
            game_world.remove_object(self)

    def draw(self):
        if not self.monster.alive:
            return

        cam = game_world.camera

        hp_ratio = max(0, min(1, self.monster.hp / self.max_hp))
        image_index = int((1 - hp_ratio) * 50)
        image_index = max(0, min(50, image_index))

        hp_bar_y = self.monster.y + 30

        if cam:
            sx, sy = cam.to_camera(self.monster.x, hp_bar_y)
        else:
            sx, sy = self.monster.x, hp_bar_y

        img = MonsterHPBar.images[image_index]
        img_w = img.w
        img_h = img.h

        display_w = 60
        scale = display_w / img_w
        display_h = img_h * scale

        img.draw(sx, sy, display_w, display_h)

    def get_bb(self):
        return 0, 0, 0, 0

    def handle_collision(self, group, other):
        pass

class Heart:
    image = None

    def __init__(self, x, y):
        if Heart.image is None:
            Heart.image = load_image('asset/hp/hearts.png')
        self.x = x
        self.y = y
        self.frame = 0
        self.alive = True

    def update(self):
        self.frame = (self.frame + 4 * game_framework.frame_time) % 4

    def draw(self):
        cam = game_world.camera
        if cam:
            sx, sy = cam.to_camera(self.x, self.y)
        else:
            sx, sy = self.x, self.y

        frame_index = int(self.frame)
        Heart.image.clip_draw(frame_index * 20, 0, 20, 18, sx, sy, 40, 36)

        if game_framework.show_bb:
            if cam:
                l, b, r, t = self.get_bb()
                sl, sb = cam.to_camera(l, b)
                sr, st = cam.to_camera(r, t)
                draw_rectangle(sl, sb, sr, st)
            else:
                draw_rectangle(*self.get_bb())

    def get_bb(self):
        if not self.alive:
            return 0, 0, 0, 0
        return self.x - 20, self.y - 18, self.x + 20, self.y + 18

    def handle_collision(self, group, other):
        if group == 'player:heart' and self.alive:
            self.alive = False
            game_world.remove_object(self)
