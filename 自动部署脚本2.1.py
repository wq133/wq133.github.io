#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import time


def runCmd(cmd):
    res = subprocess.Popen(cmd,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)

    # 该方法和子进程交互,返回一个包含 输出和错误的元组,如果对应参数没有设置的,则无法返回
    res_out, res_err = res.communicate()

    # 输出信息
    print(f'进程ID: {res.pid} \n'  # 子进程的进程ID
          f'进程的返回码: {res.returncode} \n'  # 进程的返回码.如果进程未结束,将返回None
          f'是否出错: {res_err}',  # 错误内容
          str(res_out, 'utf-8'),  # 输出内容
          sep='\n')


def countdown(t):
    while t > 0:
        print('{}s 秒后自动关闭！'.format(t))
        time.sleep(1)
        t -= 1

if __name__ == '__main__':
    cmd1 = 'git pull'                       # 拉取代码
    cmd2 = 'git add .'                      # 添加文件到git
    cmdt = input("请输入提交代码的备注：")  # 添加键入备注的变量
    cmd3 = 'git commit -m '+'"'+cmdt+'"'    # 提交备注
    cmd4 = 'git push -u origin master'      # 推送代码

    time.sleep(1)

    print('执行 git pull 命令！')
    runCmd(cmd1)        
    time.sleep(2)

    print('执行 git add . 命令！')
    runCmd(cmd2) 
    time.sleep(2)

    print('执行 git commit -m "update blog" 命令！')
    runCmd(cmd3)
    time.sleep(2)

    print('执行 git push -u origin master 命令！')
    runCmd(cmd4)  
    time.sleep(2)

    print("上传成功！！！\n")      # 提示成功
    countdown(5)
