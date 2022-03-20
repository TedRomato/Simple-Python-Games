import os
import sys
sys.path.append(os.path.abspath("C:/Users/vaine/Desktop/algopython"))
from show_pressed_keys import show_pressed_keys




from play import *
from random import randint



game_over_text = play.new_text('Game over', y = 20)
game_over_text.hide()
restart_text = play.new_text('Press r to play again', y = -20)
restart_text.hide()
score_text = play.new_text('Score: ', y = 250, x = -50)
score_display = play.new_text('0', y = 250, x = 50)

game_over = False
score = 0


ground  = play.new_box(x = 0, y = -300, width = 800, height = 200)


player = play.new_box(x = -200, y = -200,  width = 25, height = 40, color = "blue")

jumping = False
jump_state = 0
jump_height = 18 
max_flight_length = 10
flight_length = 0
'''
jump_height determines max jump_state value,
actual height in pixels can be calculated by multiplication of jump_height and jump_speed 
'''
jump_speed = 10


cactie = []


def init_cactie(number):
    i = 0
    while i < number:
        new_cactus = play.new_box(x = 0, y = -200, width = 25, height = 40, color = "green")
        cactie.append(new_cactus)
        i += 1
    


def respawn_all_cactie():
    for cactus in cactie:
        random_x = randint(420, 1200)
        cactus.x = random_x


def move_cactie(speed):
    for cactus in cactie: 
        cactus.x -= speed


def respawn_cactie():
    global score
    for cactus in cactie: 
        if(cactus.x <= -420):
            cactus.x = randint(420, 1200)
            score += 1
            score_display.words = str(score)


def handle_player_controls():
    global jumping
    if play.key_is_pressed(" ") and jump_state == 0:
       jumping = True 


def handle_jump():
    global jumping 
    global jump_state
    global flight_length

    if jump_state == jump_height:
            
            if flight_length < max_flight_length and play.key_is_pressed(" "):
                flight_length += 1
            
            else:
                jumping = False
                flight_length = 0


    if jumping and jump_state < jump_height:
        jump_state += 1
        player.y += jump_speed


    elif not jumping and jump_state > 0:
        jump_state -= 1
        player.y -= jump_speed
    

def end_game():
    global game_over
    game_over = True
    game_over_text.show()
    restart_text.show()
    score_text.hide()
    score_display.hide()

def handle_collision():
    for cactus in cactie:
        if player.is_touching(cactus):
            end_game()

def restart():
    global game_over
    global score
    respawn_all_cactie()
    score = 0
    score_display.words = str(score)
    score_display.show()
    score_text.show()
    game_over = False
    game_over_text.hide()
    restart_text.hide()


init_cactie(3)
restart()

@play.repeat_forever
def game_loop():

    show_pressed_keys(-300, 200, 25)

    global game_over
    global score
    if not game_over:

        handle_player_controls()    
        handle_jump()
        move_cactie(5)
        respawn_cactie()
        handle_collision()
        
            
        
    else:
        if play.key_is_pressed("r"):
            restart()
            

play.start_program()