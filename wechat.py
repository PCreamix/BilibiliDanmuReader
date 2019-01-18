#!/usr/bin/env python
# _*_ coding:utf-8 _*_


import itchat


class WeChat:
    def __init__(self):
        self.client = itchat.new_instance()
        self.client.auto_login()
        self.send2bilibili()

    def send2wechat(self, msg):
        self.client.send_msg(msg, toUserName='filehelper')

    def send2bilibili(self):
        @self.client.msg_register(itchat.content.TEXT)
        def danmu_reply(msg):
            print(msg)
            print(msg.fromUserName)
            print(msg.text)
        self.client.run(blockThread=False)


if __name__ == '__main__':
    c = WeChat()
    c.send2wechat('good')
    c.send2wechat('right')
    import time
    time.sleep(20)
