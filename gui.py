#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from tkinter import *
import asyncio
from asyncio import Queue
import threading


class ApplicationGUI(Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.pack()
        self.queue4log = Queue()
        self.loop = None
        self.roomid = IntVar()
        self.roomid.set(6876276)
        self.createWidgets()

    def createWidgets(self):
        self.create_operation_panel()
        self.create_loginfo_panel()

    def create_operation_panel(self):
        frm = Frame(self)
        frm.pack()
        notify_label = Label(frm, text=r'房间号：')
        notify_label.grid(row=0, column=0)
        entry = Entry(frm, textvariable=self.roomid)
        entry.grid(row=0, column=1)
        button_frame = Frame(frm)
        self.start = Button(button_frame, text=r'开始', command=self.start)
        self.start.grid(row=0, column=0)
        self.stop = Button(button_frame, text=r'停止')
        self.stop.grid(row=0, column=1)
        button_frame.grid(row=0, column=2)

    def create_loginfo_panel(self):
        frm = Frame(self)
        frm.pack()
        self.logger = Text(frm)
        self.logger.pack(side=LEFT)
        scrollbar = Scrollbar(frm, command=self.logger.yview)
        self.logger['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side=RIGHT, fill=Y)

    def logout(self, msg):
        self.logger.insert(END, '>> ')
        self.logger.insert(END, msg)
        self.logger.insert(END, '\n')
        self.logger.see(END)

    def start(self):
        # 停止旧协程和loop
        if self.loop:
            self.stop()
        # 建立新协程
        client_loop_coro = self.get_client_loop()
        log_loop_coro = self.get_log_loop()
        # 建立新loop
        self.build_new_event_loop()
        # 向新loop中添加任务
        asyncio.run_coroutine_threadsafe(client_loop_coro, self.loop)
        asyncio.run_coroutine_threadsafe(log_loop_coro, self.loop)

    def stop(self):
        if self.loop:
            try:
                self.loop.stop()
                self.loop.close()
            except:
                raise Exception('loop 有问题')
            finally:
                self.loop = None

    def get_client_loop(self):
        roomid = self.roomid.get()
        # todo: 需要用到bilibili_client内容，需要合并
        # bilibili_client 需要接收两个参数，
        # roomid: 房间号
        # queue4log: 通信管道
        pass

    async def get_log_loop(self):
        while True:
            msg = await self.queue4log.get()
            self.logout(msg)

    def build_new_event_loop(self):
        if self.loop:
            # loop存在，必须停止
            self.stop()

        self.loop = asyncio.new_event_loop()

        t = threading.Thread(target=run_loop(), args=(self.loop,))
        t.start()


def run_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def main():
    root = Tk()
    root.title(r'Bilibili Client')
    app = ApplicationGUI(root)
    app.mainloop()


if __name__ == '__main__':
    main()
