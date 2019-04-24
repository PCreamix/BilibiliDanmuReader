#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from gui import ApplicationGUI as gui
from tkinter import Tk


def main():
    root = Tk()
    root.title(r'Bilibili Client')
    app = gui(root)
    app.mainloop()


if __name__ == '__main__':
    main()
