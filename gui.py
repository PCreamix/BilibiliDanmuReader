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
        button_frame = Frame(frm)
        self.start = Button(button_frame, text=r'开始', command=self.start)
        self.start.grid(row=0, column=0)
        self.stop = Button(button_frame, text=r'停止', command=self.stop)
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

    def create_event_loop(self):
        # 建立基本循环loop,仅运行一次
        # core_loop: 客服端主要程序
        # log_loop: gui界面负责log输出，同时在需要时负责停止core_loop中任务
        self.core_loop = asyncio.new_event_loop()
        core_loop_thread = threading.Thread(target=run_loop, args=(self.core_loop,))
        core_loop_thread.start()
        self.log_loop = asyncio.new_event_loop()
        log_loop_thread = threading.Thread(target=run_loop, args=(self.log_loop,))
        log_loop_thread.start()

    async def logout(self, msg):
        self.logger.insert(END, '>> ')
        self.logger.insert(END, msg)
        self.logger.insert(END, '\n')
        self.logger.see(END)

    def start(self):
        # 负责向core_loop中注册新异步事件
        # 停止旧任务
        if self.has_tasks:
            self.stop()
        # 建立新协程
        client_loop_coro = self.get_client_loop()
        log_loop_coro = self.coro_log_loop()
        # 将新协程添加到协程core_loop中
        asyncio.run_coroutine_threadsafe(client_loop_coro, self.core_loop)
        asyncio.run_coroutine_threadsafe(log_loop_coro, self.core_loop)

    def stop(self):
        # 停止清空core_loop中的所有任务
        # 建立停止协程
        coro_stop = self.stop_core_loop_tasks()
        # 将协程注册到log_loop
        asyncio.run_coroutine_threadsafe(coro_stop, self.log_loop)
        self.has_tasks = None

    async def stop_core_loop_tasks(self):
        # 只需停止任务，无需停止core_loop
        if self.core_loop:
            while True:
                try:
                    asyncio.gather(*asyncio.Task.all_tasks(loop=self.core_loop)).cancel()
                    break  # 停止成功，将跳出循环,否则进入except
                except:
                    await asyncio.sleep(1)

    def get_client_loop(self):
        roomid = self.roomid.get()
        # todo: 需要用到bilibili_client内容，需要合并
        # bilibili_client 需要接收两个参数，
        # roomid: 房间号
        # queue4log: 通信管道
        pass

    async def coro_log_loop(self):
        while True:
            msg = await self.queue4log.get()
            await self.logout(msg)


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
