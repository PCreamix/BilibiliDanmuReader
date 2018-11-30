#!/usr/bin/env python
# _*_ coding:utf-8 _*_


class MessageHandler:
    def __init__(self, speaker, queue):
        self._speaker = speaker
        self._queue = queue

    async def read_loop(self):
        while True:
            message = await self._queue.get()
            msg_type = message[0]
            if msg_type == 'comment':
                # 弹幕消息
                text = r"{} 说 {} o".format(*(message[1:]))
            elif msg_type == 'gift':
                # 礼物消息
                text = r"谢谢{}送的{}个{} o".format(*(message[1:]))
            else:
                pass
            await self._speaker.say(text)


def main():
    print('ok')


if __name__ == '__main__':
    main()
