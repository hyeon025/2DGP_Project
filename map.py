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
            self.background = load_image(Room[current_room])
            self.world_center_x = 2500
            self.world_center_y = 2500
    def update(self):
        pass

    def draw(self):
        cam = game_world.camera
        if cam:
            # 월드 중심을 카메라로 변환해서 화면에 그림
            sx, sy = cam.to_camera(self.world_center_x, self.world_center_y)
            if current_map == "Lobby":
                self.background.draw(sx, sy, 1200, 900)
            else:
                if current_room == "Map_1" or current_room == "Map_2":
                    self.background.draw(sx, sy, 1100, 900)
                elif current_room == "Map_3" or current_room == "Map_4":
                    self.background.draw(sx, sy, 1000, 1000)
        else:
            # 카메라가 없을 때 기존 동작 유지
            if current_map == "Lobby":
                self.background.draw(600, 450, 1200, 900)
            else:
                if current_room == "Map_1" or current_room == "Map_2":
                    self.background.draw(600, 400, 1100, 900)
                elif current_room == "Map_3" or current_room == "Map_4":
                    self.background.draw(600, 400, 1000, 1000)
