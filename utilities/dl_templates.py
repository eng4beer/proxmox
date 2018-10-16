#!/usr/bin/env python

__author__ = "Scott Hamilton"
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Scott Hamilton"
__email__ = "funtimes@runcode.ninja"
__status__ = "It works....."

import sys
import subprocess

def get_available():
    ''' Check to see latest lxc available for proxmox '''
    # temp dictionary to store our data as we loop through
    available = {}
    # cheat and use some bash commands to get the initial output using subprocess
    cmd = "pveam available | awk '{print $2}' |grep -v turnkey"
    # run the command
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    # get the output from the command
    output = output.decode("ascii").strip().split()
    # loop through the data in reversed sorted order so we always get the newest entires first
    for line in sorted(output, reverse=True):
        # grap the title of the os
        os_title = line.split('-')[0]
        # if the latest title is not in our temp dict, then store it
        if os_title not in available:
            available[os_title] = line
    # return the latest lxc templates
    return available

def get_current():
    ''' Get the current templates installed on our machine, and remove duplicates '''
    # temp dictionary to store our data as we loop through
    current = {}
    # cheat and use some bash commands to get the initial output using subprocess
    cmd = "pveam list local | grep -v NAME | sed 's/.*\///' | awk '{print $1}'"
    # run the command
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    # get the output from the command
    output = output.decode("ascii").strip().split()
    # loop through the data in reversed sorted order so we always get the newest entires first
    for line in sorted(output, reverse=True):
        os_title = line.split('-')[0]
        # if the latest title is not in our temp dict, then store it
        if os_title not in current:
            current[os_title] = line
        # else if there was more than one entry, it's an older one, so remove it!
        elif os_title in current:
            print("Removing older template " + line)
            # cheat and use some bash commands to get the initial output using subprocess
            cmd = "pveam remove local:vztmpl/" + line
            # run the command
            ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            output = ps.communicate()[0]
            output = output.decode("ascii")
    return current

dups = {}
remove_older = False

if __name__ == "__main__":
    # Call the get_available function and store the output into a variable
    available = get_available()
    # Call the get_current function and store the output into a variable
    current = get_current()

    # If we have no data in our current machine, then download all the latest lxc templates
    if len(current) < 1:
        for item in available.values():
            print("Downloading " + item).strip()
            cmd = "pveam download local " + item
            ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            output = ps.communicate()[0]
            output = output.decode("ascii")

    # If we have lxc templates already installed lets do a comparison to see if what's available
    # is newer than we what have currently downloaded
    if len(current) > 0:
        for (avail_title, avail_ver), (cur_title,cur_ver) in zip(available.items(), current.items()):
            # if we found a newer version
            if avail_ver > cur_ver:
                # set a remove flag to re-run the get_current function which will clean up the duplicate
                remove_older = True
                print("Downloading " + avail_ver).strip()
                # cheat and use some bash commands to get the initial output using subprocess
                cmd = "pveam download local " + avail_ver
                # run the command
                ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                output = ps.communicate()[0]
                output = output.decode("ascii")
            # if the versions are the same, just tell them it's up to date
            elif avail_ver == cur_ver:
                print ("Skipping " + cur_ver + " as it's the latest version")
        # if there was a newer package, it set the remove_older flag to run a duplicate check
        if remove_older:
            # run the duplicate check built into the get_current function
            getlocal = get_current()
