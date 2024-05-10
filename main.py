# Import Module
import turtle
import winsound
import time
# Setup the Game Window
window = turtle.Screen()
window.title("Pong")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0)
# Game Variables
score_a = 0
score_b = 0
winner = ""
delay = 0.03
# Pens
title_pen = turtle.Turtle()
button1_pen = turtle.Turtle()
button2_pen = turtle.Turtle()
score_pen = turtle.Turtle()
winner_pen = turtle.Turtle()


def create_pen(pen, color, x, y, text, size, weight):
    pen.speed(0)
    pen.color(color)
    pen.penup()
    pen.hideturtle()
    pen.goto(x, y)
    pen.clear()
    pen.write(text, align="center", font=("Courier", size, weight))


# Buttons
button1 = turtle.Turtle()
button2 = turtle.Turtle()


def create_button(button, x, y):
    button.speed(0)
    button.shape("square")
    button.color("white")
    button.shapesize(stretch_wid=3, stretch_len=10)
    button.penup()
    button.goto(x, y)


create_button(button1, -200, -100)
create_button(button2, 200, -100)
# Mode Selection Functions
menu_running = True
single_player = False
multi_player = False


# Clears the Screen and Exits the Menu
def exit_menu():
    button1.goto(1000, 1000)
    button2.goto(2000, 2000)
    title_pen.goto(3000, 3000)
    button1_pen.goto(4000, 4000)
    button2_pen.goto(5000, 5000)
    title_pen.clear()
    button1_pen.clear()
    button2_pen.clear()
    global menu_running
    menu_running = False
    window.update()


# Starts Single PLayer Mode
def single_player_function(x, y):
    global single_player
    single_player = True
    exit_menu()


# Starts Multi Player Mode
def multi_player_function(x, y):
    global multi_player
    multi_player = True
    exit_menu()


# Mode Selection Loop (The Game Menu)
window.update()
while menu_running:
    # Display Menu Text
    create_pen(title_pen, "white", 0, 150, "PONG", 100, "normal")
    create_pen(button1_pen, "black", -200, -115, "Single-Player", 18, "normal")
    create_pen(button2_pen, "black", 200, -115, "Multi-Player", 18, "normal")
    # Button Selection Keyboard Bindings
    button1.onclick(single_player_function)
    button2.onclick(multi_player_function)

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)
# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)
# Ball
balls = []
ball1 = turtle.Turtle()
ball2 = turtle.Turtle()
ball3 = turtle.Turtle()
ball4 = turtle.Turtle()


def create_ball(name, color, dx, dy):
    name.speed(0)
    name.shape("square")
    name.color(color)
    name.penup()
    name.goto(0, 0)
    name.dx = dx
    name.dy = dy
    balls.append(name)


create_ball(ball1, "red", 2, 2)
create_ball(ball2, "blue", 1, -1)
create_ball(ball3, "yellow", -1.5, -1.5)
create_ball(ball4, "green", -1, 1)


# Functions
def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)


def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)


def paddle_b_up():
    y = paddle_b.ycor()
    if multi_player:
        y += 20
    elif single_player:
        y += 4
    paddle_b.sety(y)


def paddle_b_down():
    y = paddle_b.ycor()
    if multi_player:
        y -= 20
    elif single_player:
        y -= 4
    paddle_b.sety(y)


# Display Score
score_text = ""
if single_player:
    score_text = "Player: {}  Computer: {}"
elif multi_player:
    score_text = "Player A: {}  Player B: {}"
create_pen(score_pen, "white", 0, 260, score_text.format(score_a, score_b), 24, "normal")
# Paddle Movement Keyboard Bindings
window.listen()
window.onkeypress(paddle_a_up, "w")
window.onkeypress(paddle_a_down, "s")
if multi_player:
    window.onkeypress(paddle_b_up, "Up")
    window.onkeypress(paddle_b_down, "Down")
# Game Loop
game_running = True
while game_running:
    window.update()
    # Paddle Stopper
    if paddle_a.ycor() >= 250:
        paddle_a.sety(250)
    if paddle_a.ycor() <= -250:
        paddle_a.sety(-250)
    if paddle_b.ycor() >= 250:
        paddle_b.sety(250)
    if paddle_b.ycor() <= -250:
        paddle_b.sety(-250)
    # Loop and Take Action for each ball, multiple loops to complete one action for all balls then do next action
    for ball in balls:
        # Ball Movement
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)
    for ball in balls:
        # Ball Border Y Check
        if ball.ycor() >= 290:
            winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
            ball.sety(290)
            ball.dy *= -1
            delay -= 0.001
        if ball.ycor() <= -290:
            winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
            ball.sety(-290)
            ball.dy *= -1
            delay -= 0.001
    for ball in balls:
        # Ball Border X Check + Score Update
        if ball.xcor() >= 390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_a += 1
            create_pen(score_pen, "white", 0, 260, score_text.format(score_a, score_b), 24, "normal")
        if ball.xcor() <= -390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_b += 1
            create_pen(score_pen, "white", 0, 260, score_text.format(score_a, score_b), 24, "normal")
    for ball in balls:
        # Paddle and Ball Collisions
        if (-340 >= ball.xcor() >= -350) and (paddle_a.ycor() + 40 >= ball.ycor() >= paddle_a.ycor() - 40):
            winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
            ball.setx(-340)
            ball.dx *= -1
            delay -= 0.001
        if (340 <= ball.xcor() <= 350) and (paddle_b.ycor() + 40 >= ball.ycor() >= paddle_b.ycor() - 40):
            winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
            ball.setx(340)
            ball.dx *= -1
            delay -= 0.001
    # AI Player
    if single_player:
        closest_ball = balls[0]
        for ball in balls:
            if ball.xcor() > closest_ball.xcor():
                closest_ball = ball
        if paddle_b.ycor() < closest_ball.ycor() and abs(paddle_b.ycor() - closest_ball.ycor()) > 20:
            paddle_b_up()
        elif paddle_b.ycor() > closest_ball.ycor() and abs(paddle_b.ycor() - closest_ball.ycor()) > 20:
            paddle_b_down()
    # Winner Selector
    if single_player:
        if score_a == 10:
            winner = "Player"
            game_running = False
        elif score_b == 10:
            winner = "Computer"
            game_running = False
    elif multi_player:
        if score_a == 10:
            winner = "Player A"
            game_running = False
        elif score_b == 10:
            winner = "Player B"
            game_running = False
    # Game Speed Manager
    if delay <= 0.005:
        delay = 0.005
    time.sleep(delay)

# Game Over
# Clear Screen
for ball in balls:
    ball.goto(-1000, -1000)
paddle_a.goto(-2000, -2000)
paddle_b.goto(-3000, -3000)
# Display Message for Winner
if winner == "Player":
    create_pen(winner_pen, "white", 0, 0, "Congratulations Player, You Win!", 24, "bold")
elif winner == "Computer":
    create_pen(winner_pen, "white", 0, 0, "The Computer Wins, You Lose...", 24, "bold")
# Game Over Loop


def exit_game():
    global over_running
    over_running = False


over_running = True
while over_running:
    window.update()
    window.onkeypress(exit_game, "space")
