#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from tkinter import *


class ApplicationGUI(Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        operationPanel = self.operationPanel()
        operationPanel.pack()
        logInfoPanel = self.logInfoPanel()
        logInfoPanel.pack()

    def operationPanel(self):
        root_frame = Frame(self)
        notify_label = Label(root_frame, text=r'房间号：')
        notify_label.grid(row=0, column=0)
        self.roomid = IntVar()
        self.roomid.set(6876276)
        entry = Entry(root_frame, textvariable=self.roomid)
        entry.grid(row=0, column=1)
        button_frame = Frame(root_frame)
        self.start = Button(button_frame, text=r'开始')
        self.start.grid(row=0, column=0)
        self.stop = Button(button_frame, text=r'停止')
        self.stop.grid(row=0, column=1)
        button_frame.grid(row=0, column=2)
        return root_frame

    def logInfoPanel(self):
        root_frame = Frame(self)
        self.logger = Text(root_frame)
        self.logger.pack(side=LEFT)
        scrollbar = Scrollbar(root_frame, command=self.logger.yview)
        self.logger['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side=RIGHT, fill=Y)
        return root_frame

    def logout(self):
        self.logger.insert(END, '>> ')
        self.logger.insert(END, self.roomid.get())
        self.logger.insert(END, '\n')
        self.logger.see(END)

    def start(self):
        if self.client_loop:
            self.stop()
        roomid = self.roomid.get()

    def stop(self):
        if self.client_loop:
            # stop
            pass


def main():
    root = Tk()
    root.title(r'Bilibili Client')
    app = ApplicationGUI(root)
    app.mainloop()


if __name__ == '__main__':
    main()

# todo: gui和主程序有冲突，运行时容易卡死
