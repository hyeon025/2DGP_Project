from pico2d import load_image
import game_world

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
