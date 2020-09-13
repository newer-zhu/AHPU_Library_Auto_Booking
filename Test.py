import datetime
from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
class test:
    # 过时的方法
    def outdate(self, start_time, end_time):
        url = 'http://seat.ahpu.edu.cn:9091/tsgintf/main/service'
        # 请求头信息
        headers = {
            'Cookie': "JSESSIONID=5CC89802136333B8B7378A223D3BFD36",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'http://seat.ahpu.edu.cn:9091/tsgintf/wechat/seat/html/reserving3.html?version=1.1',
            'Host': 'seat.ahpu.edu.cn:9091',
            'Origin': 'http://seat.ahpu.edu.cn:9091',
            'Content-Length': '113',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'text/plain, */*; q=0.01'
        }
        # 请求数据
        json = {"intf_code": "QRY_PRE_SEAT",
                "params": {
                    "roomId": self.ahpu_lib['2B'],
                    "dateStr": "2020-9-11",
                    "startHour": start_time,
                    "endHour": end_time
                }
                }
        res = requests.post(url, json=json, headers=headers)
        html = res.text
        soup = BeautifulSoup(html, "lxml")
        print(soup.prettify())
        room_div = soup.find(attrs={'id': 'roomplanDiv'})
        for desk in room_div.children:
            for seat in desk.children:
                s = str(seat.attrs['class'])
                n = s[-3:-2]
                # 没有被占座
                if n == '3':
                    self.left += 1
                # 已经被占座
                elif n == '1':
                    self.seated += 1
                # 不可坐
                else:
                    self.forbid += 1
        # print("剩余座位{l}个".format(l=self.left))
    str = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')
    print(str)