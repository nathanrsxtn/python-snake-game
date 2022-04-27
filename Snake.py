#
# Copyright 2021 nathanrsxtn
#
# SPDX-License-Identifier: GPL-3.0-or-later

from random import uniform
from turtle import Screen, Turtle, Vec2D
# ------- Output Setup -------- #
screen = Screen()
screen.bgcolor("gray")
screen.title("Snake")
screen.tracer(0)
screen.setup(400, 400)
vmin = min(screen.window_width(), screen.window_height())
# ---- Game Configuration ----- #
GRID_SURROUND_U = 5 # amount of cells between the center cell and the edge
GRID_MARGIN_U = 0.5 # amount of cells between the edge and the window frame
SNAKE_SPEED = range(100, 65, -5) # start ms/tick, min ms/tick, Δ(ms/tick)/food
SNAKE_HEAD_COLOR = "dark green"
SNAKE_TAIL_COLOR = "green"
SNAKE_DEAD_TIME = 1000 # ms
FOOD_COLOR = "red"
FOOD_VALUE = 100 # score/food
FOOD_SCALE = 0.75 # %
GRASS_COLOR = "green yellow"
DISPLAY_FONT = ("System", int(vmin / 30), "normal")
SNAKE_KEY_VECTORS = [
    ( "Left", Vec2D(-True, False)),
    ("Right", Vec2D(+True, False)),
    ( "Down", Vec2D(False, -True)),
    (   "Up", Vec2D(False, +True)),
    (    "a", Vec2D(-True, False)),
    (    "d", Vec2D(+True, False)),
    (    "s", Vec2D(False, -True)),
    (    "w", Vec2D(False, +True)),
]
# ------ Game Constants ------- #
GRID_RADIUS_U = 0.5 + GRID_SURROUND_U
GRID_DIMENSION_U = 1 + (GRID_SURROUND_U * 2)
GRID_AREA_U = GRID_DIMENSION_U * GRID_DIMENSION_U
U_SIZE_PX = int(vmin / (GRID_DIMENSION_U + (GRID_MARGIN_U * 2)))
GRID_RADIUS_PX = U_SIZE_PX * GRID_RADIUS_U
GRID_DIMENSION_PX = U_SIZE_PX * GRID_DIMENSION_U
screen.highscore = 0
# -------- Input Setup -------- #
for keybind in SNAKE_KEY_VECTORS:
    def setdirection(direction=keybind[1] * U_SIZE_PX): snake.direction = direction
    screen.onkeypress(setdirection, keybind[0])
# --- Game Piece Generator ---- #
def newpiece(color, size=U_SIZE_PX):
    part = Turtle()
    part.penup()
    part.color(color)
    part.shape("square")
    part.shapesize(size / 20.0)
    return part
# -------- Game Setup --------- #
def prepare():
    # -- Current Turtle Removal --- #
    screen.reset()
    screen.turtles().clear()
    screen.update()
    # -------- Grass Setup -------- #
    newpiece(GRASS_COLOR, size=GRID_DIMENSION_PX)
    # ---- Score Display Setup ---- #
    global currentscoredisplay
    currentscoredisplay = Turtle()
    currentscoredisplay.penup()
    currentscoredisplay.hideturtle()
    currentscoredisplay.goto(-GRID_RADIUS_PX, +GRID_RADIUS_PX)
    # - High Score Display Setup -- #
    global highscoredisplay
    highscoredisplay = Turtle()
    highscoredisplay.penup()
    highscoredisplay.hideturtle()
    highscoredisplay.goto(+GRID_RADIUS_PX, +GRID_RADIUS_PX)
    highscoredisplay.write(f"High Score: {screen.highscore}" , align="right", font=DISPLAY_FONT)
    # -------- Snake Setup -------- #
    global snake
    snake = newpiece(SNAKE_HEAD_COLOR)
    snake.parts = []
    snake.direction = None
    # -------- Food Setup --------- #
    global food
    food = newpiece(FOOD_COLOR, U_SIZE_PX * FOOD_SCALE)
    food.eaten = 0
# --------- Main Loop --------- #
def tick():
    # Loose restart
    if food.eaten == -1: prepare()
    # Store head position
    lastheadpos = snake.pos()
    # Move snake head
    if snake.direction != None:
        snake.setpos(snake.pos() + (snake.direction if snake.direction != snake.parts[0].pos() - snake.pos() else -snake.direction))
    # Eat food?
    if snake.pos() == food.pos():
        food.eaten += 1
        while food.eaten + 1 < GRID_AREA_U and (food.pos() == lastheadpos or any(food.pos() == part.pos() for part in snake.parts + [snake])):
            food.setpos(round(uniform(-GRID_RADIUS_U, GRID_RADIUS_U)) * U_SIZE_PX for _ in range(2))
        snake.parts.append(newpiece(SNAKE_TAIL_COLOR))
        currentscoredisplay.clear()
        currentscoredisplay.write(f"Score: {food.eaten * FOOD_VALUE}", align="left", font=DISPLAY_FONT)
    # Move snake tail
    for i in range(len(snake.parts) - 1, -1, -1):
        # Move current part to next part position if exists, else move to head position
        snake.parts[i].goto(snake.parts[i - 1].pos() if i != 0 else lastheadpos)
        # Check if head is hitting the tail part, then loose
        if food.eaten > 1 and i != 0 and snake.pos() == snake.parts[i].pos():
            screen.highscore = max(screen.highscore, food.eaten * FOOD_VALUE)
            food.eaten = -1
    # Loose on edge collision
    if not (all(-GRID_RADIUS_PX <= cor <= GRID_RADIUS_PX for cor in snake.pos())):
        screen.highscore = max(screen.highscore, food.eaten * FOOD_VALUE)
        food.eaten = -1
    # Update output
    if food.eaten != -1: screen.update()
    # Queue next loop
    screen.ontimer(tick, SNAKE_DEAD_TIME if food.eaten == -1
        else max(SNAKE_SPEED.start + SNAKE_SPEED.step * food.eaten, SNAKE_SPEED.stop))
# ---------- Startup ---------- #
screen.listen()
prepare()
tick()
screen.mainloop()
