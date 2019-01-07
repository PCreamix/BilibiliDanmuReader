#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import random


class MessageHandler:
    def __init__(self, speaker, queue, chatbot):
        self._speaker = speaker
        self._queue = queue
        self._chatbot = chatbot

    async def read_msg(self):
        message = await self._queue.get()
        msg_type = message[0]
        text = ''
        if msg_type == 'DANMU_MSG':
            # 弹幕消息
            uname, msg, userid = message[1:]
            if uname == r'饼干喵7':
                uname = r'主播'
            if msg.startswith(r'@@'):
                # 与聊天机器人对话
                await self._chat_with_bot(uname, msg, userid)
            else:
                text = r"{}说：{} o".format(uname, msg)
        elif msg_type == 'SEND_GIFT':
            # 礼物消息
            uname, num_gift, gift_type = message[1:]
            if is_read(num_gift, gift_type):
                text = r"谢谢{}送的{}个{} o".format(uname, num_gift, gift_type)
        else:
            pass
        if text:
            await self._speaker.say(text)

    async def run(self):
        while True:
            await self.read_msg()

    async def _chat_with_bot(self, uname, msg, userid):
        # 和聊天机器人对话
        real_msg = msg.strip(r'@@')  # 取出消息具体内容
        reply = await self._chatbot.chat(userid, real_msg)  # 得到机器人的回复
        question = r'{} 对 {} 说 {} o'.format(uname, self._chatbot.name, real_msg)
        await self._speaker.say(question)
        answer = r'{}回答{}说：{} o'.format(self._chatbot.name, uname, reply)
        await self._speaker.say(answer)


def is_read(num_gift, gift_type):
    res = True
    if gift_type == r'辣条':
        if num_gift == 1:
            if random.random() > 0.23:
                res = False
    return res


def main():
    print('no test')


if __name__ == '__main__':
    main()
