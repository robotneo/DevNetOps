#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/16 13:53
# @Author  : YangHua
# @Email   : yanghuacba@outlook.com
# @File    : paramiko_learn_six
# @Software: PyCharm

import paramiko
import time

"""
Python 备份交换机配置文件FTP Server作为本机实验
"""

# 明文输出用户名
username = 'python'
# 密码输入不可见
password = 'Yanghua1012'

iplist = ['10.10.10.11', '10.10.10.12', '10.10.10.13', '10.10.10.14', '10.10.10.15']
for ip in iplist:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)

    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    print('已经成功登录交换机 ' + ip)
    command = ssh_client.invoke_shell()

    command.send('ftp 10.10.10.2\n')
    time.sleep(1)
    command.send('python\n')
    time.sleep(1)
    command.send('123456\n')
    time.sleep(1)
    command.send('binary\n')
    command.send('put vrpcfg.zip ' + ip + '_vrpcfg.zip' + '\n')
    time.sleep(1)
    command.send('bye\n')
    command.send('quit\n')
    time.sleep(1)

    output = command.recv(65535).decode('GB2312')
    print(output)

ssh_client.close()