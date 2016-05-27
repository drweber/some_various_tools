#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
from xml.etree import ElementTree as et
import fnmatch
import os
import sys

files = []
working_directory = sys.argv[1]
git_branch = sys.argv[2]
pom_version = '{http://maven.apache.org/POM/4.0.0}'

for root1, dirnames, filenames in os.walk(working_directory):
    for filename in fnmatch.filter(filenames, 'pom.xml'):
        files.append(os.path.join(root1, filename))
for file in files:
    os.system("rm -rf %sresult*.xml" % working_directory)
    tree = et.parse(file)
    root = tree.getroot()
    xmlnamespace = root.tag.split('{')[1].split('}')[0]
    try:
        parent_app_version = root.find('%sversion' % pom_version).text
    except AttributeError:
        pass
    major_version = parent_app_version.split('.')
    minor_version = str(int(major_version[1].split('-')[0])+1)
    new_app_version = str(major_version[0]) + '.' + str(minor_version) + '-SNAPSHOT'
    try:
        root.find('%sversion' % pom_version).text = new_app_version
    except AttributeError:
        root.find('%sparent/%sversion' % (pom_version, pom_version)).text = new_app_version
    print ("Version has been changed in %s" % file)
    tree.write('%sresult.xml' % working_directory)
    tree.write('%sresult.xml' % working_directory, default_namespace=xmlnamespace)
    os.system("mv -f %sresult.xml %s" % (working_directory, file))
    os.system("git add %s" % file)
os.system("mv %srest/target/%s-%s %srest/target/ROOT.war" % (working_directory, git_branch, parent_app_version,
                                                             working_directory))
os.system("git commit -m 'Update pom.xml files, current version is %s'" % new_app_version)