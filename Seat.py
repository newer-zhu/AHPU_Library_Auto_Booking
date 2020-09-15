from bs4 import BeautifulSoup
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
class Auto_Occupy(object):
    def __init__(self,username,password):
        # 浏览器对象
        # option = webdriver.ChromeOptions
        # option.headless
        self.browser = webdriver.Chrome()
        self.username = username
        self.password = password
        self.now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        #安徽工程大学图书馆楼层区域对应的roomId
        self.ahpu_lib = {
            '2A': '36', '2B': '37', '3A': '38', '3B': '39', '3C': '40', '4A': '42', '4B': '43', '4C': '44', '4E': '46',
            '5A': '47', '5B': '48',
            '5C': '49', '5D': '50', '6A': '51', '6B': '52', '6C': '53', '6D': '54', '6E': '55', '5S': '56'
        }
        # 保持登录状态所需cookie
        self.loginData = {'domain': 'seat.ahpu.edu.cn', 'httpOnly': True, 'name': 'JSESSIONID', 'path': '/tsgintf',
                          'secure': False, 'value': 'F14952287EFA449AB69F3DAE46AC86D0'}
        # 被占座位
        self.seated = 0
        # 剩余座位
        self.left = 0
        # 不可坐的
        self.forbid = 0
        # 双人座
        self.single = []
    # 发送邮件
    def sendEmail(self,text):
        # 发送者邮箱
        from_addr = '1713622254@qq.com'
        # 授权码
        password = 'uyiophxrgvsrbffc'
        # 接收者邮箱
        to_addr = '1713622254@qq.com'
        # 发信服务器
        smtp_server = 'smtp.qq.com'
        # 发送的邮件内容
        msg = MIMEText(text,'plain','utf-8')
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header('自动预约座位')

        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server,465)
        server.login(from_addr,password)
        server.sendmail(from_addr,to_addr,msg.as_string())

    # 登录
    def login(self):
        self.browser.get('http://seat.ahpu.edu.cn:9091/tsgintf/wechat/seat/html/reserving1.html?version=1.1')
        wait = WebDriverWait(self.browser, 2)
        # 登录
        try:
            UN = wait.until(EC.presence_of_element_located((By.ID, 'username')))
            PW = wait.until(EC.presence_of_element_located((By.ID, 'password')))
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.auth_login_btn')))
        except NoSuchElementException:
            print("No Element!")
        try:
            self.browser.execute_script("arguments[0].value = '" + self.username + "';", UN)
            self.browser.execute_script("arguments[0].value = '" + self.password + "';", PW)
            self.browser.execute_script("javascript:$('.iCheck-helper').click();")
            button.click()
        except Exception:
            print("Send Error!")
            #设置Cookie
        self.loginData.clear()
        self.loginData = self.browser.get_cookie('JSESSIONID')

    #设置cookie
    def set_Cookie(self):
        self.browser.get('http://ids.ahpu.edu.cn/authserver/login?service=http%3A%2F%2Fxjwxt.ahpu.edu.cn%2Fahpu%2Flogin.action')
        self.browser.add_cookie(self.loginData)
        self.browser.get('http://seat.ahpu.edu.cn:9091/tsgintf/wechat/seat/html/reserving1.html?version=1.1')

    # 选择条件
    def choose(self,begin,over):
        lib = self.browser.find_element_by_id('libraryId')
        date = self.browser.find_element_by_id('dateStrId')
        type = self.browser.find_element_by_id('typeStrId')
        start = self.browser.find_element_by_id('startHourStrId')
        end = self.browser.find_element_by_id('endHourStrId')
        button = self.browser.find_element_by_css_selector('.aui-btn')
        self.browser.execute_script("arguments[0].value = '3';", lib)
        self.browser.execute_script("arguments[0].value = '" + self.now + "';", date)
        self.browser.execute_script("arguments[0].value = '1';", type)
        self.browser.execute_script("arguments[0].value = '" + begin + "';", start)
        self.browser.execute_script("arguments[0].value = '" + over + "';", end)
        button.click()
    # 找空位
    def search(self,place,begin,over):
        self.set_Cookie()
        # 默认执行循环
        flag = True
        try:
            self.choose(begin,over)
        except:
            print('登录过期！')
            self.login()
            self.set_Cookie()
            self.choose(begin,over)
        self.browser.execute_script("gotoReserving3Page("+self.ahpu_lib[place]+");")
        # 加载页面
        time.sleep(0.3)
        soup = BeautifulSoup(self.browser.page_source,'lxml')

        room_div = soup.find(attrs={'id': 'roomplanDiv'})
        # 是否需要抢座，目的保证每次for循环都能执行
        con = True
        for desk in room_div.children:
            # 单人座抢座
            if len(list(desk.children)) == 2:
                for ds in desk.children:
                    n = str(ds.attrs['class'])[-3:-2]
                    print(n)
                    if n == '3':
                        loc = ds.contents[0].string
                        self.single.append(loc)
                        if con:
                            flag = self.occupy(loc)
                            con = False
             # 统计
            for seat in desk.children:
                s = str(seat.attrs['class'])
                # 座位是否空闲看末尾的数字
                n = s[-3:-2]
                if n == '3':
                    self.left += 1
                elif n == '1':
                    self.seated += 1
                else:
                    self.forbid += 1
        print("空闲座位{}个，不可坐座位{}个，被占座位{}个，单人空闲座位{}个".format(self.left,self.forbid,self.seated,len(self.single)))

        self.left = 0
        self.forbid = 0
        self.seated = 0
        self.single.clear()
        return flag

    # 抢座,返回False说明不需要继续循环
    def occupy(self,location):
        try:
            self.browser.execute_script("doPreSeat('"+location+"',roomId,dateStr, getStorageItem('userPhysicalCard'), startHour, endHour);")
            self.sendEmail(""+location+"抢座成功!")
            return False
        except:
            return True


