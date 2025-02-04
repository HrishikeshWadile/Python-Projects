import turtle
import math

# Set up the screen
screen = turtle.Screen()
screen.title("Elastic Collision with Turtle")
screen.bgcolor("black")
screen.setup(width=800, height=600)

# Create a ball
ball = turtle.Turtle()
ball.shape("circle")
ball.color("white")
ball.penup()
ball.speed(0)  # Animation speed, 0 is the fastest

# Ball initial trajectory
ball.dx = 3
ball.dy = 1

# Function to move the ball
def move_ball():
    x = ball.xcor()
    y = ball.ycor()

    # Move the ball
    ball.setx(x + ball.dx)
    ball.sety(y + ball.dy)

    # Check for collision with the vertical walls (left and right)
    if ball.xcor() > 390 or ball.xcor() < -390:
        ball.setx(390 if ball.xcor() > 390 else -390)  # Prevent sticking to the wall
        angle = math.atan2(ball.dy, ball.dx)
        new_angle = math.pi - angle  # Reflect angle horizontally
        ball.dx = 3 * math.cos(new_angle)
        ball.dy = 3 * math.sin(new_angle)

    # Check for collision with the horizontal walls (top and bottom)
    if ball.ycor() > 290 or ball.ycor() < -290:
        ball.sety(290 if ball.ycor() > 290 else -290)  # Prevent sticking to the wall
        angle = math.atan2(ball.dy, ball.dx)
        new_angle = -angle  # Reflect angle vertically
        ball.dx = 3 * math.cos(new_angle)
        ball.dy = 3 * math.sin(new_angle)

# Main game loop
while True:
    screen.update()
    move_ball()

# Keep the window open
turtle.mainloop()
