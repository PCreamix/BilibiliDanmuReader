#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import requests
import time
import ujson as json


class SendDanmu:
    url = r"https://api.live.bilibili.com/msg/send"
    crsf = crsf_token = r"568e1b0346ced877c7a09fe5eab3bae9"
    color = 16777215
    fontsize = 25
    mode = 1
    rnd = str(int(time.time()))
    header = {
        'User-Agent': r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36", }
    cookie = {
        "Cookie": r"pgv_pvi=9628419072; buvid3=C08D3169-A96C-467E-BC1C-0B5FBB5AE7C921719infoc; rpdid=kwxkixqkkmdoswskwsxiw; LIVE_BUVID=ca965c035ce0dae351aafb13318e8bbf; LIVE_BUVID__ckMd5=f9b7c592d1175ca4; UM_distinctid=16507f0f766671-0c4c194f1ec0db-2711639-1fa400-16507f0f767b3; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1533903471,1533904650,1533905045,1533985635; im_notify_type_221204872=0; stardustvideo=1; CURRENT_QUALITY=80; sid=8djmtmrf; _qddaz=QD.htglvx.b2yors.jmqcrwys; _cnt_dyn=undefined; _cnt_pm=0; _cnt_notify=0; uTZ=-480; CURRENT_FNVAL=16; im_local_unread_221204872=0; LIVE_PLAYER_TYPE=2; DedeUserID=221204872; DedeUserID__ckMd5=e3eec6cb273bc15d; SESSDATA=31708cb4%2C1548774775%2C31f543c1; bili_jct=568e1b0346ced877c7a09fe5eab3bae9; fts=1546226281; im_seqno_221204872=44; finger=17c9e5f5; bp_t_offset_221204872=209446798906626423; _dfcaptcha=e8e9aa635532ad57fce787b1ef9acd25", }

    def __init__(self, roomid):
        self.roomid = roomid
        self.toBeSend = True

    def send(self, msg):
        if self.toBeSend:
            params = self.__generate_params(msg)
            response = requests.post(self.url, data=params, cookies=self.cookie, headers=self.header)
            if json.loads(response.content)['code'] != 0:
                self.toBeSend = False
                print('done')

    def __generate_params(self, msg):
        form_data = {'color': self.color, 'fontsize': self.fontsize, 'mode': self.mode, 'msg': msg,
                     'roomid': self.roomid, 'bubble': 0, 'csrf_token': self.crsf_token, 'csrf': self.crsf,
                     'rnd': 1547861986, }
        return form_data


def test():
    roomid = 6876276
    client = SendDanmu(roomid)
    client.send(r'ok')


if __name__ == '__main__':
    test()
