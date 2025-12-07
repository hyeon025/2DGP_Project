from pico2d import load_image

class LevelUI:
    images = None
    level_bar_images = None
    frame_image = None
    current_level = 1
    current_exp = 0
    max_exp = 100

    def __init__(self):
        if LevelUI.images is None:
            LevelUI.images = {}
            for i in range(1, 6):
                LevelUI.images[i] = load_image(f'asset/UI/level_{i}.png')
        if LevelUI.level_bar_images is None:
            LevelUI.level_bar_images = {}
            for i in range(5, 100, 5):
                LevelUI.level_bar_images[i] = load_image(f'asset/UI/level/level_bar_{i}.png')
        if LevelUI.frame_image is None:
            LevelUI.frame_image = load_image('asset/UI/level/level_bar_frame.png')

    def add_exp(self,amount):
        LevelUI.current_exp += amount
        while LevelUI.current_exp >= LevelUI.max_exp:
            LevelUI.current_exp -= LevelUI.max_exp
            LevelUI.current_level = min(5, LevelUI.current_level + 1)

    def update(self):
        pass

    def draw(self):
        if LevelUI.current_level in LevelUI.images:
            LevelUI.images[LevelUI.current_level].draw(50, 850, 40, 40)

        if LevelUI.frame_image:
            LevelUI.frame_image.draw(135, 860, 136, 10)

        exp_percentage = int((LevelUI.current_exp / LevelUI.max_exp) * 100)

        exp_key = (exp_percentage // 5) * 5
        if exp_key < 5:
            exp_key = 5
        if exp_key > 95:
            exp_key = 95

        if exp_key in LevelUI.level_bar_images:
            LevelUI.level_bar_images[exp_key].draw(135, 860, 136, 10)

    def get_bb(self):
        return 0, 0, 0, 0

    def handle_collision(self, group, other):
        pass
