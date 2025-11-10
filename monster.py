class Monster:
    def __init__(self,x,y,hp):
        self.x = x
        self.y = y
        self.frame = 0
        self.face_dir = 1
        self.hp = hp
        self.alive = True


    def update(self):
        pass

    def draw(self):
        pass

    def handle_collision(self, group, other):
        pass

    def get_bb(self):
        pass


