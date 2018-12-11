#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from tkinter import *
import asyncio
from queue import Queue
import threading


class ApplicationGUI(Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.pack()
        self.queue4log = Queue()
        self.roomid = IntVar()
        self.roomid.set(6876276)
        self.createWidgets()
        self.create_event_loop()
        self.has_tasks = None

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
        self.button = Button(frm, text=r'开始', command=self.start)
        self.button.grid(row=0, column=3)

    def create_loginfo_panel(self):
        frm = Frame(self)
        frm.pack()
        self.logger = Text(frm)
        self.logger.pack(side=LEFT)
        scrollbar = Scrollbar(frm, command=self.logger.yview)
        self.logger['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side=RIGHT, fill=Y)

    def log_info(self):
        while True:
            msg = self.queue4log.get(block=True)
            self.logout(msg)

    def create_event_loop(self):
        # 建立基本循环loop,仅运行一次
        # core_loop: 客服端主要程序
        # setDaemon(True):设置守护进程，主进程结束后马上无条件结束
        self.core_loop = asyncio.new_event_loop()
        core_loop_thread = threading.Thread(target=run_loop, args=(self.core_loop,))
        core_loop_thread.setDaemon(True)
        core_loop_thread.start()
        log_loop_thread = threading.Thread(target=self.log_info)
        log_loop_thread.setDaemon(True)
        log_loop_thread.start()

    def logout(self, msg):
        self.logger.insert(END, '>> ')
        self.logger.insert(END, msg)
        self.logger.insert(END, '\n')
        self.logger.see(END)

    def start(self):
        # 建立新协程
        client_loop_coro = self.get_client_loop()
        # 将新协程添加到协程core_loop中
        asyncio.run_coroutine_threadsafe(client_loop_coro, self.core_loop)
        self.button['text'] = r'退出'
        self.button['command'] = self.master.destroy

    def get_client_loop(self):
        roomid = self.roomid.get()

        # queue4info：为异步asyncio.Queue，不支持跨线程
        async def run(roomid):
            from bilibili_client import Bilibili_Client
            client = Bilibili_Client(roomid, self.queue4log)
            await client.run()

        return run(roomid)


def run_loop(loop):
    # 在线程中挂起event_loop
    asyncio.set_event_loop(loop)
    loop.run_forever()


def main():
    root = Tk()
    root.title(r'Bilibili Client')
    app = ApplicationGUI(root)
    app.mainloop()


if __name__ == '__main__':
    main()
