#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import pythoncom
import win32com.client


class Speaker:
    def __init__(self):
        self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
        self.speaker.Rate = 1.2  # 语言速度

    def say(self, text):
        # 文字转化为语言播放
        if text:
            pythoncom.CoInitialize()  # 必须使用，windows平台多线程问题
            self.speaker.Speak(text)
            pythoncom.CoUninitialize()


def main():
    import threading

    def say(spk, text):
        for a in text:
            spk.say(a)

    spk1 = Speaker()
    spk2 = Speaker()
    t1 = threading.Thread(target=say, args=(spk1, ('hello', 'world')))
    t2 = threading.Thread(target=say, args=(spk2, ('你', '好')))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    main()

# todo: 多线程有问题，多进程正常
