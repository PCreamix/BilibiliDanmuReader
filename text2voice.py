#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import asyncio
import win32com.client


class Speaker:
    def __init__(self):
        self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
        self.speaker.Rate = 1.2  # 语言速度

    async def say(self, text):
        # 文字转化为语言播放
        if text:
            self.speaker.Speak(text)


def main():
    loop = asyncio.get_event_loop()
    spk = Speaker()
    text = 1
    loop.run_until_complete(spk.say(text))


if __name__ == '__main__':
    main()
