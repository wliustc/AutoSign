# -*- coding: utf-8 -*-
# @Time    : 2017/6/26 23:15
# @Author  : Ww2zero
# @Site    : 
# @File    : SchedulerTask.py
# @Software: PyCharm
from datetime import datetime
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler

def tick():
    print('Tick! The time is: %s' % datetime.now())

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=3)#间隔3秒钟执行一次
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))