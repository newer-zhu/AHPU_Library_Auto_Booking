import Seat
import datetime
from threading import Timer
# 直接运行就行了，可以自己设置一个定时任务，基本百分百中
class major:
    def zhu(self):
        username = '3190112108'
        password = '308532'
        place = '4A'
        start = '9:00'
        end = '12:00'
        app = Seat.Auto_Occupy(username, password)
        while app.searchandPoint(place, start, end, 'A3'):
            print("运行中......")
        print("成功！欢迎使用")
    def wang(self):
        username = '3190112103'
        password = '263773'
        place = '4A'
        start = '9:00'
        end = '12:00'
        app = Seat.Auto_Occupy(username, password)
        while app.searchandPoint(place, start, end,'A2'):
            print("运行中......")
        print("成功！欢迎使用")


if __name__ == '__main__':
    m = major()
    # purpose = "2020-9-17 00:00:00"
    # satrtTime = datetime.datetime.strftime(purpose,"%Y-%m-%d %H:%M:%S")
    # now = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
    # time1 = Timer((satrtTime - now).total_seconds,m.zhu())
    # time2 = Timer((satrtTime - now).total_seconds,m.wang())
    # time1.start()
    # time2.start()
    m.wang()
    m.zhu()
        # print("输入用户名：学号")
        # username = input()
        # print("输入密码：")
        # password = input()
        # print("输入地点：格式 2A (2层A区域)")
        # place = input()
        # print("输入开始时间：(格式 12：00,根据官网只能预约当天)")
        # start = input()
        # print("输入结束时间：(间隔至少为1小时！)")
        # end = input()


