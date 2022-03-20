
import os
import sys
sys.path.append(os.path.abspath("C:/Users/vaine/Desktop/algopython"))
from show_pressed_keys import show_pressed_keys





import play


# tohle je promenna pro rychlost hrace
speed = 5


player = play.new_box(height = 50,width = 50, x=0, y=0, angle=0, size=36, transparency=100)

meteor1 = play.new_circle()


@play.repeat_forever
def game_loop():
    show_pressed_keys(-300, 200, 25)

    
    if play.key_is_pressed("d") and player.x < 400:
        player.x += speed
    if play.key_is_pressed("a") and player.x > -400:
        player.x -= speed
    if play.key_is_pressed("w") and player.y < 300:
        player.y += speed
    if play.key_is_pressed("s") and player.y > -300:
        player.y -= speed
    


play.start_program()