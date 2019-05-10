#!/usr/bin/python
#-*- coding:utf-8 -*-
import os
import sys
import paramiko
import time

router_ip = "192.168.10.1"
router_port = 22
router_user = "root"
router_pwd = "hdiotwzb210"
restart_time = 180 + 50

def ping_check(d_l):
    while True:
        backinfo = os.system("ping %s -n 1 -w 100" % router_ip)
        yield d_l.send(backinfo)

def dhcp_lease():
    status = 0
    while True:
        flag = yield status
        if flag == 0:
            status = 1
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(router_ip, router_port, router_user, router_pwd)
            except:
                time.sleep(3)
                client.connect(router_ip, router_port, router_user, router_pwd)
            print "start checking..."
            for i in range(5):
                stdin, stdout, stderr = client.exec_command("cat /var/dhcp.leases")
                stdout = stdout.read().replace("\n", ",     ")
                writetofile(stdout)
                time.sleep(1)
            writetofile("---------------------------------")
            print "write to file success!"
            status = 2
        else:
            status = 0

def writetofile(msg):
    now = time.strftime("%Y-%m-%d-%H_%M_%S :  ", time.localtime(time.time()))
    wtf = open("Log.txt", "a")
    wtf.write(now + msg + "\n")
    wtf.close()

if __name__ == "__main__":
    dl = dhcp_lease()
    dl.send(None)
    check = ping_check(dl)
    for status in check:
        if status == 2:
            print "waiting for router restarted..."
            time.sleep(restart_time)
        elif status == 0:
            time.sleep(1)
