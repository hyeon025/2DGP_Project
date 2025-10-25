from pico2d import load_image

Room = {"Map_1": "asset/Map/map1.png", "Map_2": "asset/Map/map2.png", "Map_3": "asset/Map/map3.png", "Map_4": "asset/Map/map4.png"}
Map = {"Lobby":"asset/Map/Lobby_bg.png","Round_1":Room,"Round_2":Room,"Round_3":Room}
current_map = "Lobby"
current_room = "Map_1"


class Game_Map:
    def __init__(self, current_bg):
        self.map_image = load_image(current_bg)

    def update(self):
        pass

    def draw(self):
        self.map_image.draw(600, 450,1200,900)
