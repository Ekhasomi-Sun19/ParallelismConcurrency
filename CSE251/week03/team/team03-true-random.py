import math
import random
import threading
from turtle import RawTurtle
from slow_turtles import *


def draw_square(tur, x, y, side, color='black'):
    """Draw Square"""
    tur.move(x, y)
    tur.setheading(0)
    tur.color(color)
    for _ in range(4):
        tur.forward(side)
        tur.right(90)


def draw_circle(tur, x, y, radius, color='red'):
    """Draw Circle"""
    steps = 8
    circumference = 2 * math.pi * radius
    # Need to adjust starting position so that (x, y) is the center
    x1 = x - (circumference // steps) // 2
    y1 = y
    tur.move(x1, y1 + radius)
    tur.setheading(0)
    tur.color(color)
    for _ in range(steps):
        tur.forward(circumference / steps)
        tur.right(360 / steps)


def draw_rectangle(tur, x, y, width, height, color='blue'):
    """Draw a rectangle"""
    tur.move(x, y)
    tur.setheading(0)
    tur.color(color)
    tur.forward(width)
    tur.right(90)
    tur.forward(height)
    tur.right(90)
    tur.forward(width)
    tur.right(90)
    tur.forward(height)
    tur.right(90)


def draw_triangle(tur, x, y, side, color='green'):
    """Draw a triangle"""
    tur.move(x, y)
    tur.setheading(0)
    tur.color(color)
    for _ in range(4):
        tur.forward(side)
        tur.left(120)


def draw_coord_system(tur, x, y, size=300, color='black'):
    """Draw corrdinate lines"""
    tur.move(x, y)
    for i in range(4):
        tur.forward(size)
        tur.backward(size)
        tur.left(90)


def getNextStringPos(pos: list):
    if (len(pos) == 1):
        return pos[0]
    index = random.randint(0, len(pos) - 1)
    print(
        f'{threading.current_thread().name} before, index={index}, step={pos[index]}, pos={pos}')
    step = pos.pop(index) # get and remove position at index
    return step


def draw_squares(tur, lock):
    """Draw a group of squares"""
    x_pos = [-300, -100, 100, 300] # list of the x positions
    for _ in range(4):
        x = getNextStringPos(x_pos)
        y_pos = [-300, -100, 100, 300]
        for _ in range(4):
            y = getNextStringPos(y_pos)
            lock.acquire()
            print(f'{x=},{y=}')
            draw_square(tur, x - 50, y + 50, 100)
            lock.release()


def draw_circles(tur, lock):
    """Draw a group of circles"""
    x_pos = [-300, -100, 100, 300] # list of the x positions
    for _ in range(4):
        x = getNextStringPos(x_pos)
        y_pos = [-300, -100, 100, 300]
        for _ in range(4):
            y = getNextStringPos(y_pos)
            lock.acquire()
            draw_circle(tur, x, y-2, 50)
            lock.release()


def draw_triangles(tur, lock):
    """Draw a group of triangles"""
    x_pos = [-300, -100, 100, 300] # list of the x positions
    for _ in range(4):
        x = getNextStringPos(x_pos)
        y_pos = [-300, -100, 100, 300]
        for _ in range(4):
            y = getNextStringPos(y_pos)
            lock.acquire()
            draw_triangle(tur, x-30, y-30+10, 60)
            lock.release()


def draw_rectangles(tur, lock):
    """Draw a group of Rectangles"""
    x_pos = [-300, -100, 100, 300] # list of the x positions
    for _ in range(4):
        x = getNextStringPos(x_pos)
        y_pos = [-300, -100, 100, 300]
        for _ in range(4):
            y = getNextStringPos(y_pos)
            lock.acquire()
            draw_rectangle(tur, x-10, y+5, 20, 15)
            lock.release()


def draw(tur, main_turtle):
    """Draw different shapes using threads"""
    lock = threading.Lock()
    # Draw Coors system
    tur.pensize(0.5)
    draw_coord_system(tur, 0, 0, size=375)
    tur.pensize(4)
    print('-' * 50)
    print('Start Drawing With Threads')
    tur.move(0, 0)

    thread_list = []
    thread_list.append(threading.Thread(target=draw_squares, args=(tur, lock)))
    thread_list.append(threading.Thread(target=draw_circles, args=(tur, lock)))
    thread_list.append(threading.Thread(target=draw_triangles, args=(tur, lock)))
    thread_list.append(threading.Thread(target=draw_rectangles, args=(tur, lock)))
    
    for i in thread_list:
        i.start()
    for i in thread_list:
        i.join()
    print('All drawing commands have been created')
    print(f'Number of Drawing Commands: {tur.get_command_count()}')
    # Play the drawing commands that were created
    tur.play_commands(main_turtle)
    print('Total drawing time')
    tur.clear()


def main():
    # create a Screen Object
    screen = turtle.Screen()

    # Screen configuration
    screen.setup(800, 800)

    # Make RawTurtle Object (built in Python class)
    main_turtle = turtle.Turtle()
    main_turtle.speed(0)

    # Customized CSE251 Turtle object
    turtle251 = SlowTurtle()

    draw(turtle251, main_turtle)

    # Waiting for user to close window
    turtle.done()


if __name__ == "__main__":
    main()
