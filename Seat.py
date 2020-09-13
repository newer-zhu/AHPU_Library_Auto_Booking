import requests
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
class Occupy(object):
    def __init__(self):
        self.now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        #安徽工程大学图书馆楼层区域对应的roomId
        self.ahpu_lib = {
            '2A': '36', '2B': '37', '3A': '38', '3B': '39', '3C': '40', '4A': '42', '4B': '43', '4C': '44', '4E': '46',
            '5A': '47', '5B': '48',
            '5C': '49', '5D': '50', '6A': '51', '6B': '52', '6C': '53', '6D': '54', '6E': '55', '5S': '56'
        }
        # 被占座位
        self.seated = 0
        # 剩余座位
        self.left = 0
        # 不可坐的
        self.forbid = 0
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
        browser = webdriver.Chrome()
        browser.get('http://seat.ahpu.edu.cn:9091/tsgintf/wechat/seat/html/reserving1.html?version=1.1')
        wait = WebDriverWait(browser, 5)
        try:
            username = wait.until(EC.presence_of_element_located((By.ID, 'username')))
            password = wait.until(EC.presence_of_element_located((By.ID, 'password')))
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.auth_login_btn')))
        except NoSuchElementException:
            print("No Element!")
        try:
            username.send_keys('3190112108')
            password.send_keys('308532')
            button.click()
        except Exception:
            print("Send Error!")
        return browser

    def search(self,place,begin,over):
        browser = self.login()
        try:
            lib = browser.find_element_by_id('libraryId')
            date = browser.find_element_by_id('dateStrId')
            type = browser.find_element_by_id('typeStrId')
            start = browser.find_element_by_id('startHourStrId')
            end = browser.find_element_by_id('endHourStrId')
            button = browser.find_element_by_css_selector('.aui-btn')
            browser.execute_script("arguments[0].value = '3';",lib)
            browser.execute_script("arguments[0].value = '2020-9-13';",date)
            browser.execute_script("arguments[0].value = '1';",type)
            browser.execute_script("arguments[0].value = '"+begin+"';",start)
            browser.execute_script("arguments[0].value = '"+over+"';",end)
            button.click()
        except:
            print('节点操作失败！')

        browser.execute_script("gotoReserving3Page("+self.ahpu_lib[place]+");")
        time.sleep(1)
        soup = BeautifulSoup(browser.page_source,'lxml')
        room_div = soup.find(attrs={'id': 'roomplanDiv'})
        for desk in room_div.children:
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
        print("空闲座位{}个，不可坐座位{}个，被占座位{}个".format(self.left,self.forbid,self.seated))
        # Cookies = {
        #     'domain': 'seat.ahpu.edu.cn:9091',
        #     'name': 'Cookie',
        #     'value': 'JSESSIONID=5CC89802136333B8B7378A223D3BFD36',
        #     'expires': '',
        #     'path': '/',
        #     'httpOnly': False,
        #     'HostOnly': False,
        #     'Secure': False
        # }
        # browser.add_cookie(Cookies)
        # print(browser.page_source)






if __name__ == '__main__':
    o = Occupy()
    o.search('4A','14:00','16:00')