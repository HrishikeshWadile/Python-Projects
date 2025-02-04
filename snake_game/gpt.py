from turtle import Screen, Turtle
import time
import random


def move_right():
    if snake_segments[0].heading() != 180:  # Prevent the snake from moving backward
        snake_segments[0].setheading(0)


def move_up():
    if snake_segments[0].heading() != 270:
        snake_segments[0].setheading(90)


def move_left():
    if snake_segments[0].heading() != 0:
        snake_segments[0].setheading(180)


def move_down():
    if snake_segments[0].heading() != 90:
        snake_segments[0].setheading(270)


def reset():
    global score
    for segment in snake_segments:
        segment.goto(1000, 1000)  # Move segments out of view
    snake_segments.clear()
    create_snake()
    score = 0
    update_score()
    snake_segments[0].goto(0, 0)
    snake_segments[0].setheading(0)


def create_snake():
    starting_positions = [(0, 0), (-20, 0), (-40, 0)]
    for position in starting_positions:
        add_segment(position)


def add_segment(position):
    new_segment = Turtle("square")
    new_segment.penup()
    new_segment.color("white")
    new_segment.goto(position)
    snake_segments.append(new_segment)


def extend_snake():
    add_segment(snake_segments[-1].position())


def update_score():
    score_display.clear()
    score_display.write(f"Score: {score}", align="center", font=("Times New Roman", 24, "normal"))


def place_food():
    food.goto(random.randint(-280, 280), random.randint(-260, 260))


screen = Screen()
screen.setup(600, 640)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)

snake_segments = []
create_snake()

score = 0
score_display = Turtle()
score_display.penup()
score_display.hideturtle()
score_display.color("white")
score_display.goto(0, 280)
update_score()

food = Turtle()
food.shape("circle")
food.color("red")
food.penup()
place_food()

screen.listen()
screen.onkey(move_up, "Up")
screen.onkey(move_down, "Down")
screen.onkey(move_right, "Right")
screen.onkey(move_left, "Left")
screen.onkey(reset, "r")

game_is_on = True

while game_is_on:
    screen.update()
    time.sleep(0.1)

    # Move the snake segments
    for i in range(len(snake_segments) - 1, 0, -1):
        new_x = snake_segments[i - 1].xcor()
        new_y = snake_segments[i - 1].ycor()
        snake_segments[i].goto(new_x, new_y)
    snake_segments[0].forward(20)

    # Check for collision with food
    if snake_segments[0].distance(food) < 15:
        place_food()
        extend_snake()
        score += 1
        update_score()

    # Check for collision with wall
    if (snake_segments[0].xcor() > 290 or snake_segments[0].xcor() < -290 or
            snake_segments[0].ycor() > 290 or snake_segments[0].ycor() < -290):
        game_is_on = False

    # Check for collision with itself
    for segment in snake_segments[1:]:
        if snake_segments[0].distance(segment) < 10:
            game_is_on = False

screen.mainloop()