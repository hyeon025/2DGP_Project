from pico2d import load_image

import game_world

Room = {"Map_1": "asset/Map/round1_map.png", "Map_2": "asset/Map/map2.png", "Map_3": "asset/Map/map3.png", "Map_4": "asset/Map/map4.png"}
Map = {"Lobby":"asset/Map/Lobby_bg.png","Round_1":Room,"Round_2":Room,"Round_3":Room}
current_map = "Lobby"
current_room = "Map_1"


class Game_Map:
    def __init__(self, current_bg):
        if current_map == "Lobby":
            self.background = load_image(current_bg)
            self.world_center_x = 600
            self.world_center_y = 450
        else:
            self.background = load_image(Room[current_room])
            base_cx = 1375
            base_cy = 930

            self.world_center_x = int(base_cx * 2)
            self.world_center_y = int(base_cy * 2)

    def update(self):
        pass

    def draw(self):
        cam = game_world.camera
        if cam:
            sx, sy = cam.to_camera(self.world_center_x, self.world_center_y)
            if current_map == "Lobby":
                self.background.draw(sx, sy, 1200, 900)
            else:
                w = int(self.background.w * 2)
                h = int(self.background.h * 2)
                self.background.draw(sx, sy, w, h)
        else:
            if current_map == "Lobby":
                self.background.draw(600, 450, 1200, 900)
            else:
                w = int(self.background.w * 2)
                h = int(self.background.h * 2)
                self.background.draw(self.world_center_x, self.world_center_y, w, h)
