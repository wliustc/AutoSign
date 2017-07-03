# -*- coding: utf-8 -*-
import os

import click
from apscheduler.schedulers.blocking import BlockingScheduler


def getChangeStatus():
    """
    获取变动的状态,有变动返回True,无变动返回False
    :return:True/False
    """
    os.popen('git status -s > autocommit.log')
    with open("autocommit.log", 'r', encoding='utf-8') as frst:
        if frst.readline() == '':
            return False
        else:
            return True


def CHeckPath(path):
    """
    检查输入的路径是否存在，是否是git路径
    :return : True/False
    """
    if os.path.isdir(path) == False:
        print("路径不存在")
        return False
    os.chdir(path)
    gitpath = os.path.join(os.getcwd(), '.git')
    if os.path.isdir(gitpath) == False:
        print("该路径不是git路径")
        return False
    print("每隔5分钟为您一次检查：" + path)
    # 初始化log记录
    with open("autocommit.log", 'w', encoding='utf-8') as f:
        f.write("")
    return True


def AutoGitCommit():
    print("正在检查文件夹更新...")
    if getChangeStatus():
        AddCommit()
        PushOrginMaster()


def GitScheduler():
    """
    5分钟定时调度AutoGitCommit
    """
    scheduler = BlockingScheduler()
    scheduler.add_job(AutoGitCommit, 'cron', minute='*/5')
    #scheduler.add_job(AutoGitCommit, 'cron', second='*/5')
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('Exit The Job!')


def PushOrginMaster():
    """
    提交到远程仓库
    """
    os.system(' git push ')


def AddCommit():
    """
    更新文件修改信息添加commit
    """
    os.system('git add .')
    os.popen('git status -s > autocommit.log')
    rst = ''
    with open('autocommit.log', 'r', encoding='utf-8') as frst:
        rst = frst.read()
        print("修改内容如下：")
        print(rst)
    print("正在提交修改文本..")
    os.system('git commit -m "{}"'.format(rst))


@click.command()
@click.option('--gitpath', prompt='请输入自动提交的gitpath', help='自动commit，自动push to orgin master')
def main(gitpath):
    if CHeckPath(gitpath):
        GitScheduler()


if __name__ == '__main__':
    main()
    # getChangeStatus()
