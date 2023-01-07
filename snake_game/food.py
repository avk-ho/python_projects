from turtle import Turtle
import random

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600

class Food(Turtle):

    def __init__(self) -> None:
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("white")
        self.speed(0)
        self.refresh()

    # Reposition the food
    def refresh(self):
        random_x = random.randrange((SCREEN_WIDTH/-2)+20, (SCREEN_WIDTH/2)-20)
        random_y = random.randrange((SCREEN_HEIGHT/-2)+20, (SCREEN_HEIGHT/2)-20)
        self.setpos(random_x, random_y)
