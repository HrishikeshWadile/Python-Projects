from turtle import Turtle, Screen
from random import *

timmy = Turtle()
screen = Screen()
timmy.speed(0)

screen.setup(700, 400)
timmy.penup()
timmy.setpos(-300, -150)

for i in range(0, 6):

    for j in range(0, 12):
        timmy.color(randint(0, 255) / 255, randint(0, 255) / 255, randint(0, 255) / 255)
        timmy.pendown()
        timmy.dot(25)
        timmy.penup()
        timmy.forward(50)
    if i % 2 == 0:
        timmy.left(90)
        timmy.forward(50)
        timmy.left(90)
        timmy.forward(50)
    else:
        timmy.right(90)
        timmy.forward(50)
        timmy.right(90)
        timmy.forward(50)



"""
n = 5
for i in range(0, int(360/n)):
    timmy.color(randint(0, 255)/255, randint(0, 255)/255, randint(0, 255)/255)
    timmy.circle(100)
    timmy.left(n)
"""
"""
def stay_in_screen():
    if not screen.window_width() / 2 > timmy.xcor() > -screen.window_width() / 2:
        timmy.right(180)
        timmy.forward(100)
    if not screen.window_height() / 2 > timmy.ycor() > -screen.window_height() / 2:
        timmy.right(180)
        timmy.forward(100)


screen.setup(800,600)
timmy.width(10)
timmy.speed(0)
direction = [0, 90, 180, 270]

for i in range(0, 100):
    timmy.forward(50)
    timmy.setheading(choice(direction))
    timmy.color(randint(0, 255)/255, randint(0, 255)/255, randint(0, 255)/255)
    stay_in_screen()
"""
"""
for i in range(3, 11):
    angle = 180 - ((i-2)*180/i)
    timmy.color(randint(0, 255)/255, randint(0, 255)/255, randint(0, 255)/255)
    for j in range(0, i):
        timmy.right(angle)
        timmy.forward(100)
"""
"""
def dashed_line(length):
    dash_width = length / 20
    for dash in range(10):
        timmy.forward(dash_width)
        timmy.penup()
        timmy.forward(dash_width)
        timmy.pendown()


for i in range(0, 5):
    timmy.forward(10)
    dashed_line(100)
    timmy.forward(100)
    timmy.right(90)

"""
screen.exitonclick()
