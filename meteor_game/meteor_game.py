
import os
import sys
sys.path.append(os.path.abspath("C:/Users/vaine/Desktop/algopython"))
from show_pressed_keys import show_pressed_keys



from play import *

from random import randint




def regenerate_meteors(meteors):

    for meteor in meteors:
        meteor.x = randint(-400,400)
        meteor.y = 340


player = play.new_box(x = 0, y = -200, width = 25, height = 25, color = "lightseagreen")

def handle_player_movement():
    if play.key_is_pressed("a") and player.x > -400:
            player.x = player.x - 5

    if play.key_is_pressed("d") and player.x < 400:
        player.x = player.x + 5


meteors = [
    play.new_circle(radius = 10, y = 30, color="black"),
    play.new_circle(radius = 10, y = 30, color="black"),
    play.new_circle(radius = 10, y = 30, color="black"),
    play.new_circle(radius = 10, y = 30, color="black"),
    play.new_circle(radius = 10, y = 30, color="black")
]

game_over_text = play.new_text('Game over', y = 20)
game_over_text.hide()
restart_text = play.new_text('Press r to play again', y = -20)
restart_text.hide()
score_text = play.new_text('Score: ', y = 250, x = -50)
score_display = play.new_text('0', y = 250, x = 50)

regenerate_meteors(meteors)

game_over = False
score = 0


@play.repeat_forever
def game_loop():

    show_pressed_keys(-300, 200, 25)

    global game_over
    global score
    if not game_over:

        handle_player_movement()    

        for i in range(len(meteors)):
            meteors[i].y -= i*0.4 + 2 + score*0.05
            if meteors[i].is_touching(player):
                game_over = True        
                game_over_text.show()
                restart_text.show()

            if meteors[i].y < -300:
                meteors[i].y = 340
                meteors[i].x = randint(-400, 400)
                score += 1
                score_display.words = str(score)
        
    else:
        if play.key_is_pressed("r"):
            score = 0
            score_display.words = str(score)
            game_over = False
            game_over_text.hide()
            restart_text.hide()
            regenerate_meteors(meteors)
play.start_program()


