#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/13 17:38
# @Author  : YangHua
# @Email   : yanghuacba@outlook.com
# @File    : paramiko_learn_two
# @Software: PyCharm

import paramiko
import time
import getpass

# 明文输出用户名
username = input('Username: ')
# 密码输入不可见
password = getpass.getpass('Password: ')

for i in range(11, 16):
    ip = "10.10.10." + str(i)   # 整数需要转化字符串
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)
    print("Successfully connected ", ip)
    command = ssh_client.invoke_shell()
    command.send("system-view\n")
    for n in range(10, 21):
        print("Creating VLAN " + str(n))
        command.send("vlan " + str(n) + "\n")
        command.send("description Python_VLAN " + str(n) + "\n")
        time.sleep(0.5)

    command.send("return\n")
    command.send("save\n")
    command.send("y\n")
    time.sleep(2)
    output = command.recv(65535)
    print(output.decode("ascii"))


ssh_client.close()

