from pico2d import *
import time
import game_framework
import play_mode as start_mode
import round1

open_canvas(1200,900)

round1.preload_backgrounds()

game_framework.run(start_mode)

close_canvas()