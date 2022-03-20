import play


player1 = play.new_box(x = 380, y = 0, width = 10, height = 100)
player1_score = 0
player2 = play.new_box(x = -380, y = 0, width = 10, height = 100)
player2_score = 0
player_speed = 5

score_display = play.new_text(x = 0, y = 200)

ball = play.new_circle(x = 0, y = 0, radius = 5)
ball_x_speed = 4
ball_y_speed = 4

#borders 

top_border = play.new_box(x = 0, y = 300, width = 800, height = 20)
bot_border = play.new_box(x = 0, y = -300, width = 800, height = 20)
right_border = play.new_box(x = 400, y = 0, width = 20, height = 600)
left_border = play.new_box(x = -400, y = 0, width = 20, height = 600)

def handle_player_movement():
    if play.key_is_pressed("w") and not player1.is_touching(top_border):
        player1.y += player_speed
    if play.key_is_pressed("s") and not player1.is_touching(bot_border):
        player1.y -= player_speed
    if play.key_is_pressed("k") and not player2.is_touching(top_border):
        player2.y += player_speed
    if play.key_is_pressed("m") and not player2.is_touching(bot_border):
        player2.y -= player_speed


def handle_ball_movement():
    ball.x += ball_x_speed
    ball.y += ball_y_speed

def handle_bounce():
    global ball_y_speed
    global ball_x_speed

    if ball.is_touching(top_border) or ball.is_touching(bot_border):
        ball_y_speed = -ball_y_speed

    if ball.is_touching(player1) or ball.is_touching(player2):
        ball_x_speed = -ball_x_speed


def respawn_ball():
    global ball_x_speed

    ball.x = 0
    ball.y = 0
    ball_x_speed = -ball_x_speed


def update_score_display():
    score_display.words = str(player1_score) + " : " + str(player2_score)


async def check_for_goal():
    global player1_score
    global player2_score


    if ball.is_touching(right_border):
        player1_score += 1 
        respawn_ball()
        update_score_display()
        await play.timer(seconds=1)

    if ball.is_touching(left_border):
        player2_score += 1 
        respawn_ball()
        update_score_display()
        await play.timer(seconds=1)


update_score_display()

@play.repeat_forever
async def game_loop():
    handle_player_movement()
    handle_ball_movement()
    handle_bounce()
    await check_for_goal()



play.start_program()