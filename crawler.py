#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import aiohttp
import asyncio
import struct
import ujson as json
from collections import namedtuple
import requests


class Crawler:
    user_agent = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    headers = {'User-Agent': user_agent, 'Connection': 'Upgrade', }
    url = r'wss://broadcastlv.chat.bilibili.com:443/sub'
    HEADER_STRUCT = struct.Struct('>I2H2I')
    HeaderTuple = namedtuple('HeaderTuple', ('total_len', 'header_len', 'proto_ver', 'operation', 'sequence'))

    def __init__(self, uid):
        self._id = uid
        self.generate_crawl_params()

    def get_room_info(self):
        response = requests.get(url=r'https://api.live.bilibili.com/room/v1/Room/room_init', params={'id': self._id, })
        self.roomid = response.json()['data']['room_id']
        print(self.roomid)

    def generate_crawl_params(self):
        self.get_room_info()
        self.generate_auth_code()
        self.generate_heartbeat_code()
        self._websocket = None

    def _pack_params(self, data, code):
        body = json.dumps(data).encode('utf-8')
        header = self.HEADER_STRUCT.pack(self.HEADER_STRUCT.size + len(body), self.HEADER_STRUCT.size, 1, code, 1)
        return header + body

    def generate_auth_code(self):
        auth_params = {'uid': 0, 'roomid': self.roomid, 'protover': 1, 'platform': 'web', 'clientver': '1.4.0', }
        auth_code = CommunicationCode.AUTH_CODE
        self.AUTH_CODE = self._pack_params(auth_params, auth_code)

    def generate_heartbeat_code(self):
        heartbeat_params = {}
        heartbeat_code = 2
        self.HEART_BEAT = self._pack_params(heartbeat_params, heartbeat_code)

    async def crawl(self):
        while True:
            try:
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.ws_connect(self.url) as ws:
                        self._websocket = ws  # 保存链接，供全局使用
                        await self._send_auth_code()
                        async for res in ws:
                            await self._handle_message(res.data)
            except Exception as e:
                print(e)
                # 发生错误，休息一段时间，重新连接
                await asyncio.sleep(5)
            finally:
                self._websocket = None

    async def heart_beat_loop(self):
        while True:
            try:
                if self._websocket is None:
                    await asyncio.sleep(0.5)
                else:
                    await self._send_heart_beat()
                    await asyncio.sleep(30)
            except Exception as e:
                print(e)
                raise ("Can not send heart-beat!!!")

    async def _send_heart_beat(self):
        await self._websocket.send_bytes(self.HEART_BEAT)

    async def _send_auth_code(self):
        await self._websocket.send_bytes(self.AUTH_CODE)

    async def _handle_popularity(self, msg, header):
        popularity = int.from_bytes(msg[header.header_len: header.total_len], 'big')
        # print("当前直播间热度：{}".format(popularity))
        pass

    async def analysis_comment(self, comment):
        comment_time = comment[0][4]
        comment_msg = comment[1]
        comment_uname = comment[2][1]
        print(comment_time, comment_msg, comment_uname)

    async def analysis_gift(self, gift):
        gift_name = gift['giftName']
        gift_num = gift['num']
        gift_uname = gift['uname']
        print(gift_name, gift_num, gift_uname)

    async def phase_message(self, message):
        msg_type = message['cmd']
        if msg_type == 'DANMU_MSG':
            # 弹幕评论消息
            comment = message['info']
            await self.analysis_comment(comment)
        elif msg_type == 'SEND_GIFT':
            # 礼物消息
            gift = message['data']
            await self.analysis_gift(gift)
        # elif msg_type == 'ROOM_RANK':
        #     # 房间排名信息
        #     pass
        # elif msg_type == 'WELCOME':
        #     # 欢迎信息
        #     welcome = msg_type['data']
        # elif msg_type == 'SYS_MSG':
        #     # 系统消息,其它房间抽奖信息
        #     pass
        # elif msg_type == 'NOTICE_MSG':
        #     # 注意消息
        #     pass
        # elif msg_type == 'WELCOME_GUARD':
        #     # 欢迎房管
        #     pass
        # elif msg_type == 'GUARD_MSG':
        #     # 房管消息
        #     pass
        # elif msg_type == 'COMBO_END':
        #     # end of combo
        #     pass
        # else:
        #     print(msg_type)
        #     print(msg.keys())
        else:
            # 仅处理上面的弹幕和礼物消息，其它的忽略
            pass

    async def _handle_cmd(self, msg):
        # 单条消息格式都一致，为header + message形式，server连续发送
        # client单次接收可能为多条消息连续叠加，每次取一条消息处理
        while True:
            try:
                # 取header部分，如果为空字符串，则不能解读
                header = self.HeaderTuple(*self.HEADER_STRUCT.unpack_from(msg, 0))
            except struct.error:
                break
            # 取出单独一条消息处理
            message = json.loads(msg[header.header_len: header.total_len])
            await self.phase_message(message)
            # 更新读取剩下消息
            msg = msg[header.total_len:]

    async def _handle_message(self, msg):
        header = self.HeaderTuple(*self.HEADER_STRUCT.unpack_from(msg, 0))
        if header.operation == CommunicationCode.RECV_HEARTBEAT:
            # 收到服务器发送的HEATER_BEAT
            # 客服端需要返回HEATER_BEAT
            await self._send_heart_beat()
        elif header.operation == CommunicationCode.POPULARITY:
            # 服务器返回当前房间的热度信息
            await self._handle_popularity(msg, header)
        elif header.operation == CommunicationCode.COMMAND:
            # 消息从服务器发送过来，需要具体分类处理
            await self._handle_cmd(msg)
        else:
            # 未见过代码
            pass


class CommunicationCode:
    # 服务器客服端已知通讯代码
    SEND_HEARTBEAT = 2
    POPULARITY = 3
    COMMAND = 5
    AUTH_CODE = 7
    RECV_HEARTBEAT = 8


def main():
    roomid = 1111
    c = Crawler(roomid)
    tasks = [asyncio.ensure_future(c.crawl()), asyncio.ensure_future(c.heart_beat_loop())]
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt as e:
        print(asyncio.Task.all_tasks())
        for task in asyncio.Task.all_tasks():
            print(task.cancel())
        loop.stop()
        loop.run_forever()
    except Exception as e:
        print(e)
    finally:
        loop.close()


if __name__ == '__main__':
    main()

# todo: 函数名称优化
# todo: asyncio loop 中断操作确认
