import sys

from tkinter import Tk, Label, Button, Text, WORD, W, LEFT

import sys
import time

import random

import threading


class AskBox:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        window_width = 700
        window_height = 600

        self.master.geometry('%dx%d' % (window_width, window_height))

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()
        self.close_button.grid(row=0, column=0)

        self.yes_button = Button(master, text="Yes", command=self.answer_yes)
        self.yes_button.pack()
        self.yes_button.grid(row=0, column=1)

        self.no_button = Button(master, text="No", command=self.answer_no)
        self.no_button.pack()
        self.no_button.grid(row=0, column=2)

        self.rows = []

    def _answer(self, answer):
        sys.stdout.write(answer + '\n')
        sys.stdout.flush()
        oldest_row = self.rows[0]
        oldest_row.pack_forget()
        self.rows = self.rows[1:]
        for i, row in enumerate(self.rows):
            row.grid(row=i + 1)
        oldest_row.destroy()

    def answer_yes(self):
        self._answer('yes')

    def answer_no(self):
        self._answer('no')

    def add_question(self, text):
        label = Label(self.master, text=text, font=("Helvetica", 40))
        label.grid(row=len(self.rows) + 1, column=4)
        self.rows.append(label)
        self.master.update()


def add_messages():
    global my_gui
    while True:
        value = sys.stdin.readline()
        my_gui.add_question(value.strip())
        sys.stdin.flush()

if __name__ == '__main__':
    root = Tk()
    my_gui = AskBox(root)
    t = threading.Thread(target=add_messages)
    t.daemon = True
    t.start()
    root.mainloop()