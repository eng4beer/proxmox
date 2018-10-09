#!/usr/bin/env python

import sys
import subprocess

def get_available():
    cmd = "pveam available | awk '{print $2}' |grep -v turnkey"
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    output = output.decode("ascii").strip().split()
    return output

def get_local():
    cmd = "pveam list local | grep -v NAME | sed 's/.*\///' | awk '{print $1}'"
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    output = output.decode("ascii").strip().split()
    return output

newest = {}
current = {}
to_remove = {}

if __name__ == "__main__":
    available = get_available()
    getlocal = get_local()

    for line in sorted(getlocal, reverse=True):
        os_title = line.split('-')[0]
        if os_title not in current:
            current[os_title] = line

    for line in sorted(available, reverse=True):
        os_title = line.split('-')[0]
        if os_title not in newest:
            newest[os_title] = line

    for (k,v), (k2,v2) in zip(newest.items(), current.items()):
        if v > v2:
            print v2 + " is newer than than " + v
            to_remove[os_title] = v2

    if to_remove:
        for item in to_remove.values():
            print("Removing older template " + item)
            cmd = "pveam remove " + item
            ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            output = ps.communicate()[0]
            output = output.decode("ascii")

    if len(current) < 1:
        for item in newest.values():
            print("Downloading " + item).strip()
            cmd = "pveam download local " + item
            ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            output = ps.communicate()[0]
            output = output.decode("ascii")

    for (k,v), (k2,v2) in zip(newest.items(), current.items()):
        if v > v2 or k not in current:
            print("Downloading " + item).strip()
            cmd = "pveam download local " + item
            ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            output = ps.communicate()[0]
            output = output.decode("ascii")
        elif v == v2:
            print ("Skipping " + v + " as it's the latest version")
