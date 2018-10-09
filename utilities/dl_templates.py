#!/usr/bin/env python
# The purpose of this code is to automate downloading the latest containers for proxmox
import sys
import subprocess

cmd = "pveam available | awk '{print $2}' |grep -v turnkey"

ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
output = ps.communicate()[0]
output = output.decode("ascii")

final = {}

if __name__ == "__main__":
    stuff = output.strip().split()
    for line in sorted(stuff, reverse=True):
        os_title = line.split('-')[0]
        if os_title not in final:
            final[os_title] = line

for shit in final.values():
    print("Downloading " + shit).strip()
    cmd = "pveam download local " + shit
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    output = output.decode("ascii")
