from tkinter import Tk, Label, Button, Text, WORD, W, LEFT

import sys
import time

import random

import threading


class AlertBox:
    def __init__(self, master, alert_text):
        self.master = master
        master.title("A simple GUI")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        window_width = 700
        window_height = 200

        x = random.randint(0, screen_width - window_width)
        y = random.randint(0, screen_height - window_height)
        self.master.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

        self.label = Label(master, text=alert_text, fg="red", bg="black", font=("Helvetica", 40), anchor=W, justify=LEFT)
        self.label.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()


    def timeout_kill(self):
        time.sleep(10)
        self.master.quit()


if '__main__' == __name__:
    root = Tk()
    my_gui = AlertBox(root, sys.argv[1])
    t = threading.Thread(target=my_gui.timeout_kill)
    t.daemon = True
    t.start()
    root.after(1000, lambda: root.focus_force())
    root.mainloop()
