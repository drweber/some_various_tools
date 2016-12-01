#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import os
import sys

dns_names = ['akamai.bintray.com',
             'jcenter.bintray.com',
             'maven.fabric.io',
             'fabric.io',
             'crashlytics.com',
             'repo.maven.apache.org',
             'google.com',
             'updates.jenkins-ci.org',
             'repo.us-west-1.amazonaws.com',
             'pkg.jenkins-ci.org',
             'ftp-chi.osuosl.org',
             'services.gradle.org',
             'downloads.gradle.org',
             's3.amazonaws.com',
             'repo.jfrog.org',
             'fastdl.mongodb.org',
             'distribution-uploads.crashlytics.com',
             'services.gradle.org',
             'cm.crashlytics.com']

os.system("rm -rf list_of_dns.txt")
os.system("touch list_of_dns.txt")

for dns in dns_names:
    os.system('dig +short %s | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" >> list_of_dns.txt' % (dns))

#os.system("sed -e :a -e '$!N;s/\n/,/;ta' list_of_dns.txt > list_of_dns.txt")
#print ips
