import time
import threading
from turtle import Turtle, Screen
from food import Food
import tkinter


class Environment:
    def __init__(self):
        self.food = Food()
        self.screen = Screen()
        self.segments = []
        self.score = 0
        self.score_display = Turtle()
        self.can_turn = True  # Flag to control turning
        self.turn_delay = 0.001  # Time delay in seconds before next turn can be made
        self.last_turn_time = time.time()  # Initialize last turn time
        with open("highscore.txt") as highest_score:
            self.highscore = int(highest_score.read())

    def screen_setup(self):
        self.screen.setup(670, 710)
        self.screen.bgcolor("black")
        self.screen.tracer(0)
        self.boundaries()
        self.score_displayer()
        self.create_snake()
        self.screen.update()
        self.screen.mainloop()

    def create_snake(self):
        positions = [(-20, -50), (0, -50), (20, -50)]
        for position in positions:
            self.add_segments(position)
        self.snake_movement()

    def add_segments(self, position):
        segment = Turtle()
        segment.penup()
        segment.color("white")
        segment.shape("square")
        segment.goto(position)
        self.segments.append(segment)

    @staticmethod
    def boundaries():
        line = Turtle()
        line.pencolor("white")
        line.penup()
        line.setpos(-310, 280)
        line.pendown()
        line.setpos(310, 280)
        line.setpos(310, -320)
        line.setpos(-310, -320)
        line.setpos(-310, 280)
        line.hideturtle()

    def score_displayer(self):
        self.score_display.penup()
        self.score_display.pencolor("white")
        self.score_display.setpos(-167.5, 300)
        self.score_display.write(arg=f"Score : {self.score}", align="center", font=("Times New Roman", 24, "normal"))
        self.score_display.setpos(167.5, 300)
        self.score_display.write(arg=f"Highscore : {self.highscore}", align="center", font=("Times New Roman", 24, "normal"))
        self.score_display.hideturtle()

    def update_score(self):
        self.score_display.clear()
        self.score_display.setpos(-167.5, 300)
        self.score_display.write(arg=f"Score : {self.score}", align="center", font=("Times New Roman", 24, "normal"))
        self.highscore_calculator()
        self.score_display.setpos(167.5, 300)
        self.score_display.write(arg=f"Highscore : {self.highscore}", align="center",
                                 font=("Times New Roman", 24, "normal"))

    def snake_movement(self):

        self.screen.listen()
        self.screen.onkey(fun=self.move_right, key="Right")
        self.screen.onkey(fun=self.move_left, key="Left")
        self.screen.onkey(fun=self.move_up, key="Up")
        self.screen.onkey(fun=self.move_down, key="Down")

        game_is_on = True
        while game_is_on:

            self.screen.update()
            time.sleep(0.1)

            for seg_num in range(len(self.segments)-1, 0, -1):
                new_x = self.segments[seg_num - 1].xcor()
                new_y = self.segments[seg_num - 1].ycor()
                self.segments[seg_num].goto(new_x, new_y)
            self.segments[0].shape("triangle")
            self.segments[0].shapesize(stretch_len=1.5, stretch_wid=1)
            self.segments[0].forward(20)
            self.check_wall_collision()
            self.check_tail_collision()
            self.food_collision()

    def move_right(self):
        if self.can_turn and self.segments[0].heading() != 180 and time.time() - self.last_turn_time > self.turn_delay:
            self.segments[0].setheading(0)
            self.last_turn_time = time.time()
            self.can_turn = False
            self.screen.ontimer(self.allow_turn, int(self.turn_delay * 1000))

    def move_left(self):
        if self.can_turn and self.segments[0].heading() != 0 and time.time() - self.last_turn_time > self.turn_delay:
            self.segments[0].setheading(180)
            self.last_turn_time = time.time()
            self.can_turn = False
            self.screen.ontimer(self.allow_turn, int(self.turn_delay * 1000))

    def move_up(self):
        if self.can_turn and self.segments[0].heading() != 270 and time.time() - self.last_turn_time > self.turn_delay:
            self.segments[0].setheading(90)
            self.last_turn_time = time.time()
            self.can_turn = False
            self.screen.ontimer(self.allow_turn, int(self.turn_delay * 1000))

    def move_down(self):
        if self.can_turn and self.segments[0].heading() != 90 and time.time() - self.last_turn_time > self.turn_delay:
            self.segments[0].setheading(270)
            self.last_turn_time = time.time()
            self.can_turn = False
            self.screen.ontimer(self.allow_turn, int(self.turn_delay * 1000))

    def allow_turn(self):
        self.can_turn = True

    def food_collision(self):
        if self.segments[0].distance(self.food) < 15:
            self.score += 1
            self.update_score()
            self.extend()
            self.food.refresh()

    def check_wall_collision(self):
        if self.segments[0].xcor() > 310 or self.segments[0].xcor() < (-310) or self.segments[0].ycor() < (-320) or self.segments[0].ycor() > 280:
            self.endgame()

    def check_tail_collision(self):
        # Use threading to handle the delay without blocking the main thread
        threading.Thread(target=self.tail_collision_check).start()

    def tail_collision_check(self):
        time.sleep(2)
        for segment in self.segments[1:]:
            if self.segments[0].distance(segment) < 10:
                self.endgame()

    def reset(self):
        self.screen.clear()
        highscore = self.highscore
        self.__init__()
        self.highscore = highscore
        self.screen_setup()

    def highscore_calculator(self):
        if self.score > self.highscore:
            self.highscore = self.score
            with open("highscore.txt", "w") as highest_score:
                highest_score.write(str(self.highscore))

    def endgame(self):
        game_over = Turtle()
        game_over.color("white")
        game_over.write("GAME OVER", align="center", font=("Arial", 36, "normal"))
        game_over.hideturtle()
        self.screen.update()

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
            self.reset()

        def exit_game():
            root.destroy()
            self.screen.bye()

        frame = tkinter.Frame(root)
        frame.pack(pady=20)

        label = tkinter.Label(frame, text=f"Game Over!\n\nScore: {self.score}\n\nWhat would you like to do?",
                              font=("Times New Roman", 14))
        label.pack(pady=10)

        reset_button = tkinter.Button(frame, text="Reset", command=reset_game)
        reset_button.pack(side=tkinter.LEFT, padx=20)

        exit_button = tkinter.Button(frame, text="Exit", command=exit_game)
        exit_button.pack(side=tkinter.RIGHT, padx=20)

        root.deiconify()
        root.mainloop()

    def extend(self):
        self.add_segments(self.segments[-1].position())
        # new_segment = Turtle()
        # new_segment.penup()
        # new_segment.color("white")
        # new_segment.shape("square")
        # self.segments.append(new_segment)

