# from tkinter import font
from turtle import Turtle

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600
ALIGNMENT = "center"
FONT = ("Courier", 20, "normal")


class Scoreboard(Turtle):

    def __init__(self) -> None:
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.setpos(0, SCREEN_HEIGHT/2-30)
        self.score = 0
        self.display_score()

    # Write and display the score
    def display_score(self):
        self.write(arg=f"Score : {self.score}", move=False,
                   align=ALIGNMENT, font=FONT)

    # Increase the score et refresh the display
    def update_score(self):
        self.score += 1
        self.clear()
        self.display_score()
    
    # Display the game over
    def game_over(self):
        self.setpos(0, 0)
        self.color("red")
        self.write(arg=f"GAME OVER", move=False,
                   align=ALIGNMENT, font=FONT)
        
