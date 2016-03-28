#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mkarytka'

import os
import commands

ports = [22, 2200]
def remote_run(host, command):
    for port in ports:
        result = commands.getoutput("ssh root@%s -p%d %s" % (host, port, command) )
#        print port
#        print command
        print result

        if "Connection refused" not in result:
        #    print "Connection refused"
            break
    if len(result) < 2:
        result = "На %s контейнер не найден" % host
    elif len(result) > 1:
        result = "На %s контейнер найден" % host
            #break
    if "Connection refused" in result:
        result == "Connection refused"

    return result

print("Please enter container name:")
name_container = raw_input()

h = open('/home/mkarytka/git/web_deploy/tools/stagings/hosts')

#host = h.readline().strip()

for host in h.readlines():
    host = host.strip()
    if 'lxc' in name_container:
        print remote_run(host, "lxc-ls -l| grep %s| grep %s" % (name_container, name_container))
    else:
        print remote_run(host, "vzlist -a| grep %s| grep %s" % (name_container, name_container))