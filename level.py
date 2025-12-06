from pico2d import load_image

class LevelUI:
    images = None
    current_level = 1

    def __init__(self):
        if LevelUI.images is None:
            LevelUI.images = {}
            for i in range(1, 6):
                LevelUI.images[i] = load_image(f'asset/UI/level_{i}.png')

    def update(self):
        pass

    def draw(self):
        if LevelUI.current_level in LevelUI.images:
            LevelUI.images[LevelUI.current_level].draw(50, 850, 40, 40)

    def get_bb(self):
        return 0, 0, 0, 0

    def handle_collision(self, group, other):
        pass
