#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import asyncio
from crawler import Crawler
from message_handle import MessageHandler
from text2voice import Speaker
from chat_bot import ChatBot
from wechat import WeChatPipe


class Bilibili_Client:
    def __init__(self, roomid, log_print, send2wechat):
        self.send2wechat = send2wechat
        self._print = log_print
        self.queue4msg = asyncio.Queue()
        self.build_crawler(roomid)
        self.build_msg_handler()

    def build_crawler(self, roomid):
        self._crawler = Crawler(roomid, self.queue4msg, self._print)

    def build_msg_handler(self):
        spk = Speaker(self._print)
        apikey = r'fc0642ab32284058ad1e146f0c1aa0c9'
        bot_name = r'饼干侠'
        chatbot = ChatBot(apikey, bot_name)
        chatpipe = None
        if self.send2wechat:
            chatpipe = WeChatPipe(self._crawler.roomid)
        self._message_handler = MessageHandler(spk, self.queue4msg, chatbot, chatpipe, self._crawler.anchor_id)

    async def run(self):
        # 建立协程
        crawl_loop = self._crawler.run()
        reader_loop = self._message_handler.run()
        # 建立任务
        tasks = [asyncio.ensure_future(crawl_loop), asyncio.ensure_future(reader_loop), ]
        # 运行任务
        await asyncio.wait(tasks)


if __name__ == '__main__':
    roomid = 6876276

    client = Bilibili_Client(roomid, print)

    loop = asyncio.get_event_loop()
    coroutine = client.run()
    task = asyncio.ensure_future(coroutine)
    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt as e:
        print(asyncio.Task.all_tasks())
        print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
        loop.stop()
        loop.run_forever()
    finally:
        loop.close()
