from turtle import Screen, Turtle
import time
import random
import tkinter

segments = []
score = 0
food_snake = None
mega_food_snake = None
mega_food_timer = None
mega_food_chance = 0.1  # 10% chance for mega food


def move_right():
    """To move the snake to the right direction"""
    if segments[0].heading() != 180:
        segments[0].setheading(0)


def move_up():
    """To move the snake to the upper direction"""
    if segments[0].heading() != 270:
        segments[0].setheading(90)


def move_left():
    """To move the snake to the left direction"""
    if segments[0].heading() != 0:
        segments[0].setheading(180)


def move_down():
    """To move the snake to the down direction"""
    if segments[0].heading() != 90:
        segments[0].setheading(270)


def reset():
    global segments, score
    """To reset the game to start again"""

    screen.clearscreen()
    screen_setup()
    score = 0
    create_food()
    create_snake()


def screen_setup():
    global score_display

    screen.setup(640, 660)
    screen.bgcolor("black")
    screen.title("Snake Game")
    screen.tracer(0)

    score_display = Turtle()
    score_display.penup()
    score_display.color("white")
    score_display.setpos(0, 280)
    score_display.write(f"Score : {score}", align="center", font=("Times New Roman", 24, "normal"))
    score_display.hideturtle()

    line = Turtle()
    line.color("white")
    line.penup()
    line.setpos(-300, 270)
    line.pendown()
    line.setpos(300, 270)
    line.setpos(300, -310)
    line.setpos(-300, -310)
    line.setpos(-300, 270)
    line.hideturtle()

    screen.listen()
    screen.onkey(fun=move_up, key="Up")
    screen.onkey(fun=move_down, key="Down")
    screen.onkey(fun=move_right, key="Right")
    screen.onkey(fun=move_left, key="Left")
    screen.onkey(fun=reset, key="R")
    screen.onkey(fun=screen.bye, key="E")


def create_snake():
    global segments
    starting_position = [(10, 0), (-10, 0), (-30, 0)]

    segments = []
    for position in starting_position:
        add_segment(position)
    move_snake()


def add_segment(position):
    new_segment = Turtle()
    new_segment.penup()
    new_segment.color("white")
    new_segment.shape("square")
    new_segment.goto(position)
    segments.append(new_segment)


def extend():
    add_segment(segments[-1].position())


def move_snake():
    global score

    game_is_on = True

    while game_is_on:
        screen.update()
        time.sleep(0.1)
        for seg_num in range(len(segments) - 1, 0, -1):
            new_x = segments[seg_num - 1].xcor()
            new_y = segments[seg_num - 1].ycor()
            segments[seg_num].goto(new_x, new_y)

        segments[0].forward(20)

        # Check if the snake hits the wall ot tail
        if (300 < segments[0].xcor() or segments[0].xcor() < -300 or
                275 < segments[0].ycor() or segments[0].ycor() < -300):
            game_is_on = False
            display_game_over()
        head = segments[0]
        for segment in segments[1:]:
            if head.distance(segment) < 10:
                game_is_on = False
                display_game_over()

        check_food_collision()


def display_game_over():
    global score_display
    score_display.clear()
    score_display.write(f"Game Over! Score : {score}", align="center", font=("Times New Roman", 24, "normal"))
    screen.update()

    root = tkinter.Tk()
    root.title("Game Over!")
    root.withdraw()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 300) // 2  # Adjust width as needed
    y = (screen_height - 200) // 2  # Adjust height as needed

    # Set geometry to center the dialog box
    root.geometry(f"300x200+{x}+{y}")

    def reset_game():
        root.destroy()
        reset()

    def exit_game():
        root.destroy()
        screen.bye()

    frame = tkinter.Frame(root)
    frame.pack(pady=20)

    label = tkinter.Label(frame, text=f"Game Over!\n\nScore: {score}\n\nWhat would you like to do?",
                          font=("Times New Roman", 14))
    label.pack(pady=10)

    reset_button = tkinter.Button(frame, text="Reset", command=reset_game)
    reset_button.pack(side=tkinter.LEFT, padx=20)

    exit_button = tkinter.Button(frame, text="Exit", command=exit_game)
    exit_button.pack(side=tkinter.RIGHT, padx=20)

    root.deiconify()
    root.mainloop()


def create_food():
    global food_snake, mega_food_snake, mega_food_timer
    # Hide or clear the previous food
    if food_snake is not None:
        food_snake.hideturtle()  # or food_snake.clear()

    food_snake = Turtle()
    food_snake.shape("circle")
    food_snake.penup()
    food_snake.color("Blue")
    food_snake.shapesize(stretch_wid=0.5, stretch_len=0.5)
    food_snake.speed("fastest")
    random_x = random.randrange(-290, 291, 20)
    random_y = random.randrange(-300, 276, 20)
    food_snake.goto(random_x, random_y)

    # Create mega food with a chance
    if mega_food_snake is not None:  # Check if mega_food_snake already exists
        mega_food_snake.hideturtle()  # Hide it if it exists
        mega_food_snake = None  # Reset mega_food_snake to None

    if random.random() < mega_food_chance:
        mega_food_snake = Turtle()  # Create a new mega_food_snake
        mega_food_snake.shape("circle")
        mega_food_snake.penup()
        mega_food_snake.color("Red")
        mega_food_snake.shapesize(stretch_wid=1, stretch_len=1)
        mega_food_snake.speed("fastest")
        random_x = random.randrange(-290, 291, 20)
        random_y = random.randrange(-300, 276, 20)
        mega_food_snake.goto(random_x, random_y)
        mega_food_timer = screen.ontimer(hide_mega_food, 5000)  # 5 seconds timer to hide mega food


def hide_mega_food():
    global mega_food_snake
    if mega_food_snake is not None:
        mega_food_snake.hideturtle()
        mega_food_snake = None


def check_food_collision():
    global score, food_snake, mega_food_snake
    if segments[0].distance(food_snake) < 15:  # Assuming the size of the food is 15
        extend()
        score += 1
        score_display.clear()
        score_display.write(f"Score : {score}", align="center", font=("Times New Roman", 24, "normal"))
        create_food()

    if mega_food_snake is not None and segments[0].distance(mega_food_snake) < 15:
        for i in range(5):
            extend()
        score += 5  # Mega food gives 5 points
        score_display.clear()
        score_display.write(f"Score : {score}", align="center", font=("Times New Roman", 24, "normal"))
        mega_food_snake.hideturtle()
        mega_food_snake = None  # Hide mega food after it's eaten


screen = Screen()
screen_setup()
reset()
screen.mainloop()
