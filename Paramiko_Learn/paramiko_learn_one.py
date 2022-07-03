#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/13 17:06
# @Author  : YangHua
# @Email   : yanghuacba@outlook.com
# @File    : paramiko_learn_one
# @Software: PyCharm

import paramiko
import time

ip = "10.10.10.11"
username = "python"
password = "Yanghua1012"

# 创建SSH对象
ssh_client = paramiko.SSHClient()
"""
默认情况下，Paramiko模块会拒绝任何未知的SSH public key, 
这里我们使用set_missing_host_key_policy(paramiko.AutoAddPolicy)
来让Paramiko接受来自SSH Server端提供的public key
"""
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)
print("Successfully connected ", ip)

# invoke_shell()方法，将其assign给command这个变量
command = ssh_client.invoke_shell()

# SSH对象调用invoke_shell()方法，并调用send()方法
command.send("system-view\n")
command.send("undo interface LoopBack 0\n")
# command.send("interface vlanif 1\n")
# command.send("ip address 10.10.10.15 24\n")
command.send("return\n")
command.send("save\n")
command.send("y\n")

time.sleep(3)
command.send("display this\n")
time.sleep(1)

# python截屏本次运行script后的所有输出记录，将其assign给output这个变量
output = command.recv(65535)
# python3回显是字节型字符串，需要进行转换，转换成字符串
print(output.decode("ascii"))
# 退出SSH
ssh_client.close()

