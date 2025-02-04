from turtle import Turtle, Screen
from random import randint, choice
import time


class Environment:

    def __init__(self):
        self.animal = Turtle()
        self.level = 1
        self.score = 0
        self.screen = Screen()
        self.line_positions = []
        self.car_positions = []
        self.cars = []
        self.level_display = Turtle()
        self.game_is_on = True
        self.last_car_creation_time = 0

    def screen_setup(self):
        self.screen.setup(500, 650)
        self.screen.tracer(0)
        self.start_line()
        self.level_displayer()
        self.create_animal()
        self.move_animal()
        self.generate_cars_position()
        self.generate_lines()
        self.game_loop()
        self.screen.update()
        self.screen.exitonclick()

    def create_animal(self):
        self.animal.shape("turtle")
        self.animal.penup()
        self.animal.shapesize(stretch_len=0.75, stretch_wid=1)
        self.animal.setpos(0, -302.5)
        self.animal.setheading(90)

    def reset_animal(self):
        self.animal.setpos(0, -302.5)
        self.animal.setheading(90)

    def move_animal(self):
        self.screen.listen()
        self.screen.onkey(fun=self.move_up, key="Up")
        self.screen.onkey(fun=self.move_down, key="Down")

    def move_up(self):
        self.animal.forward(25)
        self.screen.update()

    def move_down(self):
        if self.animal.ycor() > -324:
            self.animal.back(25)
        self.screen.update()

    @staticmethod
    def start_line():
        start_line = Turtle()
        start_line.penup()
        start_line.setpos(250, -287.5)
        start_line.pendown()
        start_line.setheading(180)
        start_line.pensize(2)
        start_line.forward(500)
        start_line.hideturtle()

    def generate_lines(self):
        for i in range(0, 2 + self.level):
            x = 250
            y = -262.5 + i * 25
            self.line_positions.append((x, y))
        line = Turtle()
        for position in self.line_positions:
            line.penup()
            line.setpos(position)
            line.setheading(180)
            line.pendown()
            line.forward(10)
        line.hideturtle()

    def generate_cars_position(self):
        self.car_positions = []
        for i in range(0, 2 + self.level):
            x = 250
            y = -275 + i * 25
            self.car_positions.append((x, y))

    def create_car(self):
        car = Turtle()
        car.penup()
        car.shape("square")
        car.shapesize(stretch_wid=1, stretch_len=2)
        car.setpos(choice(self.car_positions))
        car.color(randint(0, 255) / 255, randint(0, 255) / 255, randint(0, 255) / 255)
        car.setheading(180)
        self.cars.append(car)

    def move_cars(self):
        for car in self.cars:
            car.forward(5)
            if car.xcor() < -250:
                car.hideturtle()
                self.cars.remove(car)

    def car_collision(self):
        for car in self.cars:
            if self.animal.distance(car) < 20:
                self.game_over()

    def level_displayer(self):
        self.level_display.clear()
        self.level_display.penup()
        self.level_display.setpos(0, 275)
        self.level_display.write(arg=f"Level : {self.level}", align="center", font=("Times New Roman", 24, "normal"))
        self.level_display.hideturtle()

    def next_level(self):
        if self.level < 20:
            if self.animal.ycor() > self.line_positions[-1][1]:
                self.level += 1
                self.reset_animal()
                self.level_displayer()
                self.generate_cars_position()
                self.generate_lines()
        else:
            self.screen.clear()
            game_over = Turtle()
            game_over.penup()
            game_over.write(arg=f"You have reached the highest level possible", align="center",
                            font=("Times New Roman", 24, "normal"))
            game_over.hideturtle()
            time.sleep(5)
            self.screen.bye()

    def game_loop(self):
        while self.game_is_on:
            current_time = time.time()
            if current_time - self.last_car_creation_time > 2.5 / self.level:
                self.create_car()
                self.last_car_creation_time = current_time
            self.screen.update()
            self.move_cars()
            self.car_collision()
            self.next_level()
            time.sleep(0.1)

    def game_over(self):
        self.screen.clear()
        game_over = Turtle()
        game_over.penup()
        game_over.write(arg=f"Game Over!!!\nYour highest level reached is: {self.level}", align="center",
                        font=("Times New Roman", 24, "normal"))
        game_over.hideturtle()
        time.sleep(5)
        self.screen.bye()
