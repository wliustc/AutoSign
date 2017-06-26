# -*- coding: utf-8 -*-
# @Time    : 2017/6/24 21:57
# @Author  : Ww2zero
# @File    : nowcoderlogin.py
from http import cookiejar
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
import os
import click
from datetime import datetime

HEADERS = {
    "Host": "www.nowcoder.com",
    "Referer": "https://www.nowcoder.com/",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='nowcodercookies.txt')
try:
    #print(session.cookies)
    session.cookies.load(ignore_discard=True)
except:
    print("还没有cookie信息")

def login(email, password):
    login_url = 'https://www.nowcoder.com/login/do?token='
    data = {
        'email': email,
        'pwd': password,
        'remember': 'true'}
    response = session.post(login_url, data=data, headers=HEADERS)
    print(response.json())
    for i in session.cookies:
        print(i)
    session.cookies.save()

#@click.command()
#@click.option('--feel',prompt='今天的打卡心情是>',help='输入打卡内容')
def dayfeel():
    """
    每日打卡
    :param feel: 打卡内容
    :return: 打印打卡结果
    """
    feel = ('nowcoder打卡%s 加油每一天。gogogo!!' % datetime.now())
    print(feel)
    email = ""
    password = ""
    login(email, password)
    dfurl = "https://www.nowcoder.com/clock/new?token="
    data = {
        "feeling":feel
    }
    response = session.post(dfurl, data=data, headers=HEADERS)
    print(response.json())



if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(dayfeel, 'cron', second='3',minute= '5',hour = '0')
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('Exit The Job!')
