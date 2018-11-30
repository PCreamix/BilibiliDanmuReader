#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import asyncio
from crawler import Crawler
from message_handle import MessageHandler
from text2voice import Speaker


class Bilibili_Client:
    def __init__(self, crawler, message_handle):
        self._crawler = crawler
        self._message_handle = message_handle

    def run(self):
        crawl_loop = self._crawler.crawl()
        heart_beat_loop = self._crawler.heart_beat_loop()
        reader_loop = self._message_handle.read_loop()
        tasks = [asyncio.ensure_future(crawl_loop), asyncio.ensure_future(heart_beat_loop),
                 asyncio.ensure_future(reader_loop)]
        return tasks


if __name__ == '__main__':
    spk = Speaker()
    queue = asyncio.Queue()
    uid = 6876276

    reader = MessageHandler(spk, queue)
    crawler = Crawler(uid, queue)

    client = Bilibili_Client(crawler, reader)

    loop = asyncio.get_event_loop()
    tasks = client.run()
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt as e:
        loop_tasks = asyncio.Task.all_tasks()
        print(loop_tasks)
        for task in loop_tasks:
            print(task.cancel())
        loop.stop()
        loop.run_forever()
    finally:
        loop.close()
