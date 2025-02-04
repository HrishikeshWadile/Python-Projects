import random
from turtle import Turtle, Screen
# import math
import time


class Environment:

    def __init__(self):
        self.score_1 = 0
        self.score_2 = 0
        self.ball = Turtle()
        self.paddle_1 = Turtle()
        self.paddle_2 = Turtle()
        self.score = Turtle()
        self.screen = Screen()
        # self.ball.dx = random.choice([-3, -2, -1, 1, 2, 3])
        # self.ball.dy = random.choice([-3, -2, -1, 1, 2, 3])
        self.paddle_2_direction = 1
        self.angle = random.choice([random.randint(-45, -15), random.randint(15, 45),
                                    random.randint(135, 165), random.randint(195, 225)])
        self.speed = 0.2
        self.speed_increment = 0.05
        self.last_speed_increment_time = time.time()

    def game_start(self):
        while self.score_1 < 5 and self.score_2 < 5:
            self.move_ball()
            self.screen.update()
        self.game_over()

    def create_paddles(self):
        """Create the paddles for the game."""
        position_1 = (-450, -30)
        position_2 = (450, -50)
        self.paddle_1.shape("square")
        self.paddle_1.color("blue")
        self.paddle_1.shapesize(stretch_len=1, stretch_wid=5)
        self.paddle_1.penup()
        self.paddle_1.goto(position_1)
        self.paddle_2.shape("square")
        self.paddle_2.color("blue")
        self.paddle_2.shapesize(stretch_len=1, stretch_wid=5)
        self.paddle_2.penup()
        self.paddle_2.goto(position_2)

    def create_ball(self):
        """Create the ball for the game."""
        self.ball.penup()
        self.ball.color("red")
        self.ball.shape("circle")
        self.ball.shapesize(stretch_wid=1, stretch_len=1)
        y = random.randint(-350, 260)
        self.ball.setpos(0, y)
        self.ball.speed(1)
        self.ball.setheading(self.angle)

    def reset_ball(self):
        """Reset the ball to the center and set a random direction."""
        self.ball.hideturtle()
        self.ball.setpos(0, random.randint(-350, 260))
        self.angle = random.choice([random.randint(-45, 45), random.randint(135, 225)])
        self.ball.setheading(self.angle)
        self.ball.showturtle()

    @staticmethod
    def create_boundaries():
        """Create the boundaries and center line."""
        line = Turtle()
        line.color("white")
        line.penup()
        line.setpos(-500, 260)
        line.pendown()
        line.setpos(500, 260)
        line.penup()
        line.setpos(0, 350)
        line.setheading(270)
        length = 700
        dash_length = 10
        num_dash = int(length / (2 * dash_length))
        for _ in range(num_dash):
            line.pendown()
            line.forward(dash_length)
            line.penup()
            line.forward(dash_length)
        line.hideturtle()

    def move_paddle_up_1(self):
        """ Function to move paddle up """
        if self.paddle_1.ycor() < 210:
            (x, y) = self.paddle_1.position()
            self.paddle_1.setpos(x, y + 20)

    def move_paddle_down_1(self):
        """ Function to move paddle down """
        if self.paddle_1.ycor() > -280:
            (x, y) = self.paddle_1.position()
            self.paddle_1.setpos(x, y - 20)

    def move_paddle_up_2(self):
        """ Function to move paddle up """
        if self.paddle_2.ycor() < 210:
            (x, y) = self.paddle_2.position()
            self.paddle_2.setpos(x, y + 20)

    def move_paddle_down_2(self):
        """ Function to move paddle down """
        if self.paddle_2.ycor() > -280:
            (x, y) = self.paddle_2.position()
            self.paddle_2.setpos(x, y - 20)

    def paddle_movement_1(self):
        """ Function to handle paddle movement """
        self.screen.listen()
        self.screen.onkeypress(fun=self.move_paddle_up_1, key="w")
        self.screen.onkeypress(fun=self.move_paddle_down_1, key="s")
        self.screen.update()

    def paddle_movement_2(self):
        """Function to handle paddle 2 movement."""
        self.screen.listen()
        self.screen.onkeypress(fun=self.move_paddle_up_2, key="Up")
        self.screen.onkeypress(fun=self.move_paddle_down_2, key="Down")
        self.screen.update()

    def score_displayer(self):
        """Display the current score."""
        self.score.clear()
        self.score = Turtle()
        self.score.penup()
        self.score.pencolor("yellow")
        self.score.setpos(-250, 265)
        self.score.write(arg=f"Score : {self.score_1}", align="center", font=("Times New Roman", 48, "normal"))
        self.score.setpos(250, 265)
        self.score.write(arg=f"Score : {self.score_2}", align="center", font=("Times New Roman", 48, "normal"))
        self.score.hideturtle()

    # Function to move the ball
    # noinspection SpellCheckingInspection
    def move_ball(self):

        # x = self.ball.xcor()
        # y = self.ball.ycor()

        # Increase speed every 3 seconds
        current_time = time.time()
        if current_time - self.last_speed_increment_time >= 3:
            self.speed += self.speed_increment
            self.last_speed_increment_time = current_time

        # Move the ball
        self.ball.forward(self.speed)

        # Reflect angle if the ball hits top or bottom boundary
        if self.ball.ycor() > 259 or self.ball.ycor() < -339:
            self.ball.setheading(-self.ball.heading())

        if (self.ball.distance(self.paddle_2) < 50 and self.ball.xcor() > 439 or
                self.ball.distance(self.paddle_1) < 50 and self.ball.xcor() < -439):
            self.ball.setheading(180-self.ball.heading())
        # Move the ball
        # self.ball.setx(x + self.ball.dx)
        # self.ball.sety(y + self.ball.dy)

        # # Check for collision with the vertical walls (left and right)
        # # if self.ball.xcor() > 390 or self.ball.xcor() < -390:
        # #     self.ball.setx(390 if self.ball.xcor() > 390 else -390)  # Prevent sticking to the wall
        # #     angle = math.atan2(self.ball.dy, self.ball.dx)
        # #     new_angle = math.pi - angle  # Reflect angle horizontally
        # #     self.ball.dx = 3 * math.cos(new_angle)
        # #     self.ball.dy = 3 * math.sin(new_angle)
        #
        # if self.ball.distance(self.paddle_1) < 10 or self.ball.distance(self.paddle_1) < 10:
        #     self.ball.dx *= -1
        #
        # # Check for collision with the horizontal walls (top and bottom)
        # if self.ball.ycor() > 260 or self.ball.ycor() < -350:
        #     self.ball.sety(260 if self.ball.ycor() > 260 else -350)  # Prevent sticking to the wall
        #     angle = math.atan2(self.ball.dy, self.ball.dx)
        #     new_angle = -angle  # Reflect angle vertically
        #     self.ball.dx = 1 * math.cos(new_angle)
        #     self.ball.dy = 1 * math.sin(new_angle)

        if self.ball.xcor() > 490:
            self.speed = 0.2
            self.reset_ball()
            self.score_1 += 1
            self.score_displayer()

        if self.ball.xcor() < (-490):
            self.speed = 0.2
            self.reset_ball()
            self.score_2 += 1
            self.score_displayer()

    def game_over(self):
        """Display game over message."""
        self.score.clear()
        self.score.goto(0, 0)
        self.score.write("Game Over", align="center", font=("Times New Roman", 48, "normal"))
        self.score.goto(0, -50)
        if self.score_1 >= 5:
            self.score.write("Player 1 Wins!", align="center", font=("Times New Roman", 24, "normal"))
        elif self.score_2 >= 5:
            self.score.write("Player 2 Wins!", align="center", font=("Times New Roman", 24, "normal"))

    def screen_setup(self):
        """Set up the game screen and initialize all components."""
        self.screen.setup(1000, 700)
        self.screen.tracer(0)
        self.screen.bgcolor("black")
        self.screen.title("Pong")
        self.create_boundaries()
        self.create_paddles()
        self.create_ball()
        self.score_displayer()
        self.paddle_movement_1()
        self.paddle_movement_2()
        self.screen.update()
        self.game_start()
        self.screen.mainloop()
