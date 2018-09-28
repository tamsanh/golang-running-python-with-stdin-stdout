"""
Adapted from ZetCode Tkinter tutorial by Jan Bodnar at zetcode.com
"""

import json
import sys
import random

import time
from PIL import Image, ImageTk, ImageOps, ImageColor
from tkinter import Tk, Frame, Canvas, ALL, NW
import threading


class Cons:
    BOARD_WIDTH = 1000
    BOARD_HEIGHT = 1000
    DELAY = 100
    DOT_SIZE = 10
    MAX_RAND_POS = 27


class Direction:
    def __init__(self, choose=None):
        self.moveX = 0
        self.moveY = 0

        if choose == None:
            choose = random.randint(0, 4)
        if choose == 0:
            self.up()
        elif choose == 1:
            self.down()
        elif choose == 2:
            self.left()
        else:
            self.right()

    def left(self):
        self.moveX = -Cons.DOT_SIZE
        self.moveY = 0

    def right(self):
        self.moveX = Cons.DOT_SIZE
        self.moveY = 0

    def up(self):
        self.moveX = 0
        self.moveY = -Cons.DOT_SIZE

    def down(self):
        self.moveX = 0
        self.moveY = Cons.DOT_SIZE


class Board(Canvas):
    def __init__(self):
        super().__init__(width=Cons.BOARD_WIDTH, height=Cons.BOARD_HEIGHT,
                         background="black", highlightthickness=0)

        self.initGame()
        self.pack()

    def initGame(self):
        self.createSnake('initial')
        self.bind_all("<Key>", self.onKeyPressed)
        self.after(Cons.DELAY, self.onTimer)

    snakes = {}
    snake_images = {}

    def createSnake(self, snake_id, choose=None):
        '''creates new snakes on Canvas'''

        color1 = tuple([random.randint(0, 256),random.randint(0, 256),random.randint(0, 256) ])
        color2 = tuple([random.randint(0, 256),random.randint(0, 256),random.randint(0, 256)])

        head = ImageTk.PhotoImage(Image.new('RGB', [10, 10], color1))
        dot = ImageTk.PhotoImage(Image.new('RGB', [10, 10], color2))

        self.snake_images['head-' + snake_id] = head
        self.snake_images['dot-' + snake_id] = dot

        start_x = random.randint(0, Cons.BOARD_WIDTH / 10 - 1) * 10
        start_y = random.randint(0, Cons.BOARD_HEIGHT / 10 - 1) * 10

        self.create_image(start_x, start_y, image=head, anchor=NW, tag="head-%s" % snake_id)
        self.create_image(start_x - 10, start_y, image=dot, anchor=NW, tag="dot-%s" % snake_id)
        self.create_image(start_x - 20, start_y, image=dot, anchor=NW, tag="dot-%s" % snake_id)

        self.snakes[snake_id] = Direction(choose)

    def updateMoveState(self, state):
        for k, v in state.items():
            if k not in self.snakes:
                self.createSnake(k)
            if v == "UP":
                self.snakes[k].up()
            elif v == "DOWN":
                self.snakes[k].down()
            elif v == "LEFT":
                self.snakes[k].left()
            elif v == "RIGHT":
                self.snakes[k].right()

    def _wrapOutOfBounds(self, head):

        x1, y1, x2, y2 = self.bbox(head)
        if x1 < 0:
            self.coords(head, (Cons.BOARD_WIDTH - Cons.DOT_SIZE, y1))

        if x1 > Cons.BOARD_WIDTH - Cons.DOT_SIZE:
            self.coords(head, (0, y1))

        if y1 < 0:
            self.coords(head, (x1, Cons.BOARD_HEIGHT - Cons.DOT_SIZE))

        if y1 > Cons.BOARD_HEIGHT - Cons.DOT_SIZE:
            self.coords(head, (x1, 0))

    def moveSnakes(self):
        for snake_id, dir in self.snakes.items():
            dots = self.find_withtag("dot-%s" % snake_id)
            head = self.find_withtag("head-%s" % snake_id)

            items = dots + head

            z = 0
            while z < len(items) - 1:
                c1 = self.coords(items[z])
                c2 = self.coords(items[z + 1])
                self.move(items[z], c2[0] - c1[0], c2[1] - c1[1])
                z += 1

            self.move(head, dir.moveX, dir.moveY)
            self._wrapOutOfBounds(head)

    def onKeyPressed(self, e):
        """
        Allow control of the initial snake
        """

        key = e.keysym

        dir = self.snakes["initial"]
        LEFT_CURSOR_KEY = "Left"
        if key == LEFT_CURSOR_KEY:
            dir.moveX = -Cons.DOT_SIZE
            dir.moveY = 0

        RIGHT_CURSOR_KEY = "Right"
        if key == RIGHT_CURSOR_KEY:
            dir.moveX = Cons.DOT_SIZE
            dir.moveY = 0

        RIGHT_CURSOR_KEY = "Up"
        if key == RIGHT_CURSOR_KEY:
            dir.moveX = 0
            dir.moveY = -Cons.DOT_SIZE

        DOWN_CURSOR_KEY = "Down"
        if key == DOWN_CURSOR_KEY:
            dir.moveX = 0
            dir.moveY = Cons.DOT_SIZE

    def onTimer(self):
        self.moveSnakes()
        self.after(Cons.DELAY, self.onTimer)


class Worm(Frame):
    def __init__(self):
        super().__init__()

        self.master.title('Snake')
        self.board = Board()
        self.pack()


def main():
    root = Tk()
    nib = Worm()

    def update_movement():
        while True:
            raw_state = sys.stdin.readline()
            state = json.loads(raw_state)
            nib.board.updateMoveState(state)
            sys.stdin.flush()

    t = threading.Thread(target=update_movement)
    t.daemon = True
    t.start()

    root.mainloop()


if __name__ == '__main__':
    main()