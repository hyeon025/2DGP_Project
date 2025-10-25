from pico2d import load_image

Room = {"Map_1": "asset/Map/map1.png", "Map_2": "asset/Map/map2.png", "Map_3": "asset/Map/map3.png", "Map_4": "asset/Map/map4.png"}
Map = {"Lobby":"asset/Map/Lobby_bg.png","Round_1":Room,"Round_2":Room,"Round_3":Room}
current_map = "Lobby"
current_room = "Map_1"


class Game_Map:
    def __init__(self, current_bg):
        if current_map == "Lobby":
            self.background = load_image(current_bg)
        else:
            self.background = load_image(Room[current_room])
    def update(self):
        pass

    def draw(self):
        if current_map == "Lobby":
            self.background.draw(600, 450, 1200, 900)
        else:
            if current_room == "Map_1" or current_room == "Map_2":
                self.background.draw(600, 400, 1100, 900)
            elif current_room == "Map_3" or current_room == "Map_4":
                self.background.draw(600, 400, 1000, 1000)
