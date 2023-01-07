# https://www.udemy.com/course/100-days-of-code/learn/lecture/20356587#overview

# Days 20 and 21

# Snake game project

# Step 1 - Creating the snake body
# Step 2 - Move the snake
# Step 3 - Control the snake
# Step 4 - Detect collision with the food
# Step 5 - Create a scoreboard
# Step 6 - Detect collision with wall
# Step 7 - Detect collision with tail

from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600

screen = Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.bgcolor("black")
screen.title("Snake game")
screen.tracer(0) # Step 2

# Step 1 - Creating the snake body
# "Head" of the snake must be at (0, 0), each section is 20*20
# Snake has 3 parts at the beginning, the body being at the left of the head

# head = Turtle(shape="square")
# head.color("white")

# body1 = Turtle(shape="square")
# body1.color("white")
# body1.setpos(-20, 0)

# body2 = Turtle(shape="square")
# body2.color("white")
# body2.setpos(-40, 0)

####

# segments = []
# for i in range(3):
#     new_segment = Turtle(shape="square")
#     new_segment.color("white")
#     new_segment.penup()
#     new_segment.setpos(-20*i, 0)
#     segments.append(new_segment)

snake = Snake()
food = Food()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(snake.up, "z")
screen.onkey(snake.down, "s")
screen.onkey(snake.left, "q")
screen.onkey(snake.right, "d")

# Step 2 - Move the snake

game_over = False
while not game_over:
    screen.update()
    time.sleep(0.1)

    snake.move()
    
    # Detect collision with food
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreboard.update_score()
    
    # Detect collision with walls
    if snake.head.xcor() < -280 or snake.head.xcor() > 280 or snake.head.ycor() < -280 or snake.head.ycor() > 280:
        game_over = True
        scoreboard.game_over()

    # Detect collision with tail
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            game_over = True
            scoreboard.game_over()

screen.exitonclick()