#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/13 22:23
# @Author  : YangHua
# @Email   : yanghuacba@outlook.com
# @File    : paramiko_learn_three
# @Software: PyCharm

import paramiko
import time
import getpass

# 明文输出用户名
username = input('Username: ')
# 密码输入不可见
password = getpass.getpass('Password: ')

# open()函数打开文件 readlines()函数读取全部文件内容 逐行读取
file = open("ip_list.txt", mode="r")        # 打开txt文件
for line in file.readlines():            # 循环读取每行的数据
    ip = line.strip()       # 移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)
    print("成功连接交换机：", ip)
    # invoke_shell()方法，将其assign给command这个变量
    remote_connection = ssh_client.invoke_shell()
    # 交换机的命令输入到代码里面 不够灵活
    remote_connection.send("system-view\n")
    remote_connection.send("dis cur interface Vlanif 1\n")
    remote_connection.send("return\n")
    remote_connection.send("save\n")
    remote_connection.send("y\n")

    time.sleep(1)
    output = remote_connection.recv(65535)
    print(output.decode("ascii"))

file.close()
ssh_client.close()
