from turtle import Turtle

MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0
STARTING_POSITION = [(0, 0), (-20, 0), (-40, 0)]

class Snake:

    def __init__(self) -> None:
        self.segments = []
        self.create_body()
        self.head = self.segments[0]

    # Create the initial body of the snake
    def create_body(self):
        for i in range(3):
            self.add_segment(STARTING_POSITION[i])

    # Add a segment to the snake
    def add_segment(self, position):
        new_segment = Turtle(shape="square")
        new_segment.color("white")
        new_segment.penup()
        new_segment.setpos(position)
        self.segments.append(new_segment)

    # Add a segment to the emplacement of the last segment
    def extend(self):
        self.add_segment(self.segments[-1].position())
    
    # Moving the segments starting from the tail to the head
    def move(self):
        for seg_idx in reversed(range(len(self.segments))):
            if seg_idx > 0:
                next_seg_pos = self.segments[seg_idx-1].pos()
                self.segments[seg_idx].setpos(next_seg_pos[0], next_seg_pos[1])
            else:
                self.segments[seg_idx].forward(MOVE_DISTANCE)

    # Direct the head up
    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    # Direct the head down
    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    # Direct the head right
    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)

    # Direct the head left
    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)
