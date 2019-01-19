#!/usr/bin/env python
# _*_ coding:utf-8 _*_


import itchat
from send_danmu import SendDanmu


class WeChatPipe:
    def __init__(self, roomid):
        self.client = itchat.new_instance()
        self.client.auto_login()
        self.smtp = SendDanmu(roomid)
        self.send2audience()

    def send2wechat(self, msg):
        self.client.send_msg(msg, toUserName='filehelper')

    def send2audience(self):
        @self.client.msg_register(itchat.content.TEXT)
        def danmu_reply(msg):
            msg = msg.text
            if msg.startswith(r"##"):
                self.smtp.send(msg.lstrip(r"##"))

        self.client.run(blockThread=False)


def main():
    roomid = 6876276

    c = WeChatPipe(roomid)
    c.send2wechat('good')
    import time

    time.sleep(20)


if __name__ == '__main__':
    main()
