class Camera:
    def __init__(self, world_w, world_h, screen_w, screen_h):
        self.world_w = world_w
        self.world_h = world_h
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.x = 0
        self.y = 0

    def update(self, x, y):
        cx = x - self.screen_w // 2 #중심
        cy = y - self.screen_h // 2

        cx = max(0, min(cx, self.world_w - self.screen_w))
        cy = max(0, min(cy, self.world_h - self.screen_h))
        self.x, self.y = cx, cy

    def to_camera(self, world_x, world_y):
        return world_x - self.x, world_y - self.y