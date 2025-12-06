from pico2d import load_font

class Letter:
    font = None

    @staticmethod
    def init():
        if Letter.font is None:
            Letter.font = load_font('asset/UI/letter.TTF', 30)

    @staticmethod
    def draw_number(x, y, number, color=(255, 255, 255)):
        Letter.init()
        Letter.font.draw(x, y, str(number), color)
