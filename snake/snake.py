import os
import sys
sys.path.append(os.path.abspath("C:/Users/vaine/Desktop/algopython"))







from random import randrange
from math import ceil
import play


# game state variables

running = True
score = 0



# window & resolution 

cell_size = 25
rows = (play.screen.height)/cell_size - 1
columns = (play.screen.width)/cell_size - 1
border_width = (play.screen.height - rows*cell_size)/2


# background

borders = play.new_box(x=0,y=0,border_width=border_width, border_color="brown", color="yellow", width = play.screen.width, height = play.screen.height)
from show_pressed_keys import show_pressed_keys

# labels and text

game_over_text = play.new_text('Game over', y = 20)
game_over_text.hide()
restart_text = play.new_text('Press r to play again', y = -20)
restart_text.hide()
score_text = play.new_text('Score: ', y = 250, x = -50)
score_display = play.new_text('0', y = 250, x = 50)



def generate_cell(x,y,color):
    return play.new_box(x = x*cell_size, y = y*cell_size, color = color, width = cell_size,height = cell_size)


# game variables

snake = []
direction = ""
has_eaten = False


# starting coordinates of fruit
fruit_start_x = 0
fruit_start_y = 2

fruit = generate_cell(fruit_start_x,fruit_start_y,"green")



def setup_game():
    global snake
    global fruit
    global direction
    global score


    # delete all cells of old snake
    for cell in snake:
        cell.remove()
    
    snake = []


    # spawning new snake
    snake.append(generate_cell(0,0,"red"))
    snake.append(generate_cell(0,-1,"black"))

    direction = "up"

    # spawning new fruit
    fruit.remove()
    fruit = generate_cell(fruit_start_x,fruit_start_y,"green")

    # reseting score to zero
    score = 0

    # handle labels
    game_over_text.hide()
    restart_text.hide()
    score_text.show()
    score_display.show()



@play.when_program_starts
def setup():
    setup_game()







def update_direction():
    global direction

    # when snake is moving horizontaly, direction can change to vertical
    if direction == "up" or direction == "down":
        
        if play.key_is_pressed("a"):
            direction = "left"

        if play.key_is_pressed("d"):
            direction = "right"

    # when snake is moving verticaly, direction can change to horizontal

    elif direction == "left" or direction == "right":
        
        if play.key_is_pressed("w"):
            direction = "up"

        if play.key_is_pressed("s"):
            direction = "down"


def move_snake():
    global has_eaten
    
    # get index of last snake cell
    i = len(snake) -  1

    # if snake has eaten, add new cell to the end (this one won't be moved)
    if has_eaten:
        snake.append(generate_cell(snake[i].x, snake[i].y, "black"))
        has_eaten = False 
    
    # move every cell to the place of a cell before this one
    while i > 0:
        snake[i].x = snake[i - 1].x
        snake[i].y = snake[i - 1].y
        i = i - 1

    # move head   
    if direction == "up":
        snake[i].y = snake[i].y + cell_size
    if direction == "down":
        snake[i].y = snake[i].y - cell_size
    if direction == "left":
        snake[i].x = snake[i].x - cell_size
    if direction == "right":
        snake[i].x = snake[i].x + cell_size



def respawn_fruit():

    fruit_touching_snake = True

    # generate new coordinates for fruit until it doesn't touch any part of snake
    while fruit_touching_snake:

        fruit_touching_snake = False

        # calculate max cell coordinates
        max_x = ceil(columns/2) - 1
        max_y = ceil(rows/2) - 1

        # move fruit
        fruit.x = randrange(-max_x, max_x) * cell_size
        fruit.y = randrange(-max_y, max_y) * cell_size    
 
        # check if fruit didn't get spawned in any a position of any snake cell
        for cell in snake:
            if cell.is_touching(fruit):
                fruit_touching_snake = True


def handle_fruit_collision():

    global has_eaten
    global score

    if snake[0].is_touching(fruit):

        # remember, that snake ate fruit
        has_eaten = True

        # move fruit to a random location
        respawn_fruit()

        #update score display
        score = score + 1
        score_display.words = str(score)



def game_over_callback():
    global running
    running = False

    # display game over information
    game_over_text.words = 'Score achived: ' + str(score)
    game_over_text.show()
    restart_text.show()

    # hide texts from active part of the game
    score_text.hide()
    score_display.hide()



def handle_snake_collision():

    # check if snake head touches any of the other cells
    i = len(snake) - 1
    while i > 0:
        if snake[0].is_touching(snake[i]):

            # end the game
            game_over_callback()

        i = i - 1

# check if snake is on the playfield 
def handle_border_collision():

    # calculate border distance from screen center
    max_x = columns/2*cell_size
    max_y = rows/2*cell_size

    # end the game if snake is out of borders
    if snake[0].x > max_x or snake[0].x < -max_x: 
        game_over_callback()

    if snake[0].y > max_y or snake[0].y < -max_y: 
        game_over_callback()


@play.repeat_forever
async def game_loop():
    global running
    show_pressed_keys(-300, 200, 25)


    if running:
        # calculate delay between game iterations ( more score means shorter delay)
        pause_between_iterations = max(0.1 - (int(score/4)) * 0.01, 0.01)
        await play.timer( seconds = pause_between_iterations )
        update_direction()
        move_snake()
        handle_fruit_collision()
        handle_snake_collision()
        handle_border_collision()

    elif play.key_is_pressed("r"):
        
        setup_game()
        running = True



play.start_program()