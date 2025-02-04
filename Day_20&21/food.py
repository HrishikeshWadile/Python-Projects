from turtle import Turtle
import random


class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("blue")
        self.penup()
        self.speed("fastest")
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.refresh()

    def refresh(self):
        random_x = random.randrange(-300, 300, 20)
        random_y = random.randrange(-310, 270, 20)
        self.setpos(random_x, random_y)
