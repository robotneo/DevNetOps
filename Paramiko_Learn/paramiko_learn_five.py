#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/15 16:53
# @Author  : YangHua
# @Email   : yanghuacba@outlook.com
# @File    : paramiko_learn_five
# @Software: PyCharm

import paramiko
import sys
import time
import getpass
import socket

"""
处理信息错误，但不执行不中断的操作
"""

# 明文输出用户名
username = input('Username: ')
# 密码输入不可见
password = getpass.getpass('Password: ')

ip_file = sys.argv[1]
cmd_file = sys.argv[2]

# 存放认证失败的设备信息
switch_with_authentication_issue = []
# 存放网络不通的设备信息
switch_not_reachable = []

iplist = open(ip_file, 'r')
for line in iplist.readlines():
    try:
        ip = line.strip()
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)
        print("已经成功登录交换机 " + ip)
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        command = ssh_client.invoke_shell()
        cmdlist = open(cmd_file, 'r')
        cmdlist.seek(0)     # 从文本内容第一标开始
        for line in cmdlist.readlines():
            each_command = line.strip()
            command.send(each_command + "\n")
            time.sleep(0.5)

        cmdlist.close()
        output = command.recv(65535).decode('ASCII')
        print(output)
    except paramiko.ssh_exception.AuthenticationException:
        print(ip + "用户验证失败")
        switch_with_authentication_issue.append(ip)
    except socket.error:
        print(ip + "目标不可达")
        switch_not_reachable.append(ip)

iplist.close()
ssh_client.close()

print('\n 下列交换机用户验证失败：')
for i in switch_with_authentication_issue:
    print(i)
print('\n 下列交换机SSH不可达：')
for i in switch_not_reachable:
    print(i)


