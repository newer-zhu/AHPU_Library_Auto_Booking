import Seat
class major:
    if __name__ == '__main__':
        print("输入用户名：学号")
        username = input()
        print("输入密码：")
        password = input()
        print("输入地点：格式 2A (2层A区域)")
        place = input()
        print("输入开始时间：(格式 12：00)")
        start = input()
        print("输入结束时间：(间隔至少为1小时！)")
        end = input()
        app = Seat.Auto_Occupy(username,password)
        while app.search(place,start,end):
            print("运行中......")
        print("成功！欢迎使用")