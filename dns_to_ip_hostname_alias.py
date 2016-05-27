#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Resolve the DNS/IP address of a given domain
data returned is in the format:
(name, aliaslist, addresslist)
"""
import socket

def getIP(d):
    """
    This method returns the first IP address string
    that responds as the given domain name
    """
    try:
        data = socket.gethostbyname(d)
        ip = repr(data)
        return ip
    except Exception:
        # fail gracefully!
        return False
#
def getIPx(d):
    """
    This method returns an array containing
    one or more IP address strings that respond
    as the given domain name
    """
    try:
        data = socket.gethostbyname_ex(d)
        ipx = repr(data[2])
        return ipx
    except Exception:
        # fail gracefully!
        return False
#
def getHost(ip):
    """
    This method returns the 'True Host' name for a
    given IP address
    """
    try:
        data = socket.gethostbyaddr(ip)
        host = repr(data[0])
        return host
    except Exception:
        # fail gracefully
        return False
#
def getAlias(d):
    """
    This method returns an array containing
    a list of aliases for the given domain
    """
    try:
        data = socket.gethostbyname_ex(d)
        alias = repr(data[1])
        return alias
    except Exception:
        # fail gracefully
        return False
#

dns_names = ['google.com','yahoo.com']
result = {}

#ip = getIP(dnsname)
#ipx = getIPx(dnsname)
#hostname = getHost(dnsname)
#alias = getAlias(dnsname)
#print " IP ", ip
#print " IPx ", ipx
#print " Host ", hostname
#print " Alias ", alias

for dnsname in dns_names:
    result[dnsname] = getHost(dnsname)

print result