#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import asyncio
from crawler import Crawler
from message_handle import MessageHandler
from text2voice import Speaker
from chat_bot import ChatBot


class Bilibili_Client:
    def __init__(self, crawler, message_handle):
        self._crawler = crawler
        self._message_handle = message_handle

    async def run(self):
        # 建立协程
        crawl_loop = self._crawler.crawl()
        heart_beat_loop = self._crawler.heart_beat_loop()
        reader_loop = self._message_handle.read_loop()
        # 建立任务
        tasks = [asyncio.ensure_future(crawl_loop), asyncio.ensure_future(heart_beat_loop),
                 asyncio.ensure_future(reader_loop)]
        # 运行任务
        await asyncio.wait(tasks)


if __name__ == '__main__':
    spk = Speaker()
    queue = asyncio.Queue()

    apikey = r'fc0642ab32284058ad1e146f0c1aa0c9'
    bot_name = r'饼干侠'
    chatbot = ChatBot(apikey, bot_name)
    uid = 6876276

    reader = MessageHandler(spk, queue, chatbot)
    crawler = Crawler(uid, queue)

    client = Bilibili_Client(crawler, reader)

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
