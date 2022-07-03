#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/14 14:25
# @Author  : YangHua
# @Email   : yanghuacba@outlook.com
# @File    : paramiko_learn_four
# @Software: PyCharm

import paramiko
import time
import getpass
import sys

"""
假设你现在手边有3台管理ip地址在10.10.10.x /24网段的3750交换机以及
3台管理ip地址在10.10.11.x/24网段的3850交换机，它们的hostname和管理ip地址如下：
S5700_1: 10.10.10.11
S5700_2: 10.10.10.12
S5700_3: 10.10.10.13
S5700_4: 10.10.10.14
S5700_5: 10.10.10.15

CE6800_1: 10.10.10.21
CE6800_2: 10.10.11.22
"""

# 明文输出用户名
username = input('Username: ')
# 密码输入不可见
password = getpass.getpass('Password: ')

ip_file = sys.argv[1]
cmd_file = sys.argv[2]

iplist = open(ip_file, 'r')     # 打开ip_file
for line in iplist.readlines():
    ip = line.strip()
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    print('已经成功登录交换机 ' + ip)
    command = ssh_client.invoke_shell()
    cmdlist = open(cmd_file, 'r')
    # seek() 方法用于移动文件读取指针到指定位置
    cmdlist.seek(0)
    for line in cmdlist.readlines():
        each_command = line.strip()
        command.send(each_command + '\n')
        time.sleep(2)
    cmdlist.close()     # 关闭文件

    # python截屏本次运行script后的所有输出记录，将其assign给output这个变量
    output = command.recv(65535).decode('ASCII')
    print(output)

iplist.close()
ssh_client.close()      # 关闭SSH客户端