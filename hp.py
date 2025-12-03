from pico2d import load_image
import game_world

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

        BossHPBar.images[image_index].draw(sx, sy, 262, 34)

    def get_bb(self):
        return 0, 0, 0, 0

    def handle_collision(self, group, other):
        pass
