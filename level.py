from pico2d import load_image

class LevelUI:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.images = {}
            cls._instance.level_bar_images = {}
            cls._instance.frame_image = None
            cls._instance.current_level = 1
            cls._instance.current_exp = 0
            cls._instance.max_exp = 100
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        for i in range(1, 6):
            self.images[i] = load_image(f'asset/UI/level_{i}.png')
        for i in range(5, 100, 5):
            self.level_bar_images[i] = load_image(f'asset/UI/level/level_bar_{i}.png')
        self.frame_image = load_image('asset/UI/level/level_bar_frame.png')

    def add_exp(self, amount):
        self.current_exp += amount
        while self.current_exp >= self.max_exp:
            self.current_exp -= self.max_exp
            self.current_level = min(5, self.current_level + 1)
            print(f"레벨 업! 현재 레벨: {self.current_level}")

    def update(self):
        pass

    def draw(self):
        if self.current_level in self.images:
            self.images[self.current_level].draw(50, 850, 40, 40)

        if self.frame_image:
            self.frame_image.draw(135, 860, 136, 10)

        # 경험치가 1 이상일 때만 레벨바 출력
        if self.current_exp > 0:
            exp_percentage = int((self.current_exp / self.max_exp) * 100)

            exp_key = (exp_percentage // 5) * 5
            if exp_key < 5:
                exp_key = 5
            if exp_key > 95:
                exp_key = 95

            if exp_key in self.level_bar_images:
                self.level_bar_images[exp_key].draw(135, 860, 136, 10)

    def get_bb(self):
        return 0, 0, 0, 0

    def handle_collision(self, group, other):
        pass
