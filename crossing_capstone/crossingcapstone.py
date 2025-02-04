import time
from turtle import Turtle, Screen
from random import *


class CrossingCapstone:

    def __init__(self):
        self.animal = Turtle()
        self.screen = Screen()
        self.line = Turtle()
        self.cars = []
        self.game_is_on = True
        self.level = 1
        self.line_position = []
        self.car_position = []
        self.level_display = Turtle()
        self.car_timers = []
        self.game_started = True

    def screen_setup(self):
        self.screen.setup(500, 600)
        self.screen.tracer(0)
        self.level_displayer()
        self.start_line()
        self.create_animal()
        self.animal_movement()
        self.generate_lines()
        self.game_loop()
        self.screen.update()
        self.screen.mainloop()

    def create_animal(self):
        self.animal.shape("turtle")
        self.animal.shapesize(stretch_len=1, stretch_wid=1)
        self.animal.penup()
        self.animal.setpos(0, -262.5)
        self.animal.setheading(90)
        self.animal.speed(0)
        time.sleep(0)

    def animal_movement(self):
        self.screen.listen()
        self.screen.onkey(fun=self.move_up, key="Up")
        self.screen.onkey(fun=self.move_down, key="Down")

    def move_up(self):
        self.animal.forward(25)
        if self.animal.ycor() > self.line_position[-1][1]:
            self.next_level()

    def move_down(self):
        if self.animal.ycor() > -300:
            self.animal.back(25)

    def generate_lines(self):
        for pos in range(0, 2 + self.level):
            y = -225 + pos * 25
            x = 250
            self.line_position.append((x, y))
            self.car_timers.append(time.time() + uniform(2.0, 3.0))  # Initialize timers for each lane

        for position in self.line_position:
            self.draw_lines(position)

    @staticmethod
    def start_line():
        start = Turtle()
        start.penup()
        start.pensize(2)
        start.setpos(250, -250)
        start.pendown()
        start.setheading(180)
        start.forward(500)
        start.hideturtle()

    def draw_lines(self, line_position):
        self.line.penup()
        self.line.setpos(line_position)
        self.line.pendown()
        self.line.back(500)
        self.line.hideturtle()

    def create_car(self):
        for i, position in enumerate(self.line_position):
            current_time = time.time()
            if current_time > self.car_timers[i]:
                car_x = 250
                car_y = position[1] - 12.5
                car = Turtle()
                car.shape("square")
                car.shapesize(stretch_wid=1, stretch_len=2)
                car.color(randint(0, 255) / 255, randint(0, 255) / 255, randint(0, 255) / 255)
                car.penup()
                car.setpos(car_x, car_y)
                car.setheading(180)
                self.cars.append(car)
                self.car_timers[i] = current_time + uniform(2.0, 4.0)

    def move_cars(self):
        for car in self.cars:
            car.forward(5)
            car.speed(1)
            if car.xcor() < -300:
                car.hideturtle()
                self.cars.remove(car)

    def animal_collision(self):
        for car in self.cars:
            if self.animal.distance(car) < 15:
                self.game_over()

    def game_loop(self):
        while self.game_is_on:
            self.screen.update()
            if self.game_started:
                self.move_cars()
                self.animal_collision()
            self.create_car()
            time.sleep(0.1)

    def level_displayer(self):
        self.level_display.clear()
        self.level_display.penup()
        self.level_display.setpos(0, 250)
        self.level_display.pendown()
        self.level_display.write(arg=f"Level : {self.level}", align="center", font=("Times New Roman", 24, "normal"))
        self.level_display.hideturtle()

    def next_level(self):
        self.level += 1
        self.animal.setpos(0, -262.5)
        self.level_displayer()
        self.generate_lines()

    def game_over(self):
        self.game_is_on = False
        self.screen.clear()
        game_over = Turtle()
        game_over.write(f"Game Over! Highest Level: {self.level}", align="center",
                        font=("Times New Roman", 24, "normal"))
        game_over.hideturtle()
        self.screen.update()
        time.sleep(2)
        self.screen.bye()
