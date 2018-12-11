#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import asyncio
import win32com.client
import pythoncom


class Speaker:
    def __init__(self, queue4log):
        self.queue4log = queue4log
        try:
            pythoncom.CoInitialize()  # 多线程中使用pywin32
            self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
        except Exception as e:
            print(e)
        self.speaker.Rate = 2.5  # 语言速度

    async def say(self, text):
        # 文字转化为语言播放
        if text:
            self.queue4log.put(text)
            self.speaker.Speak(text)


def main():
    loop = asyncio.get_event_loop()
    spk = Speaker()
    text = 1
    loop.run_until_complete(spk.say(text))


if __name__ == '__main__':
    main()
