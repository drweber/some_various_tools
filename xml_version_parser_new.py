#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
from xml.etree import ElementTree as et
import fnmatch
import os
import sys

files = []
working_directory = sys.argv[1]
# git_branch = sys.argv[2]
pom_version = '{http://maven.apache.org/POM/4.0.0}'

files.append(os.path.join(working_directory, 'pom.xml'))

file = files[0]
tree = et.parse(file)
root = tree.getroot()
xmlnamespace = root.tag.split('{')[1].split('}')[0]
minor_version = root.find('%sproperties/%sminor.version' % (pom_version, pom_version)).text
major_version = root.find('%sproperties/%smajor.version' % (pom_version, pom_version)).text
parent_app_version = '%s.%s-SNAPHOT' % (major_version, minor_version)
new_minor_version = int(root.find('%sproperties/%sminor.version' % (pom_version, pom_version)).text) + 1
root.find('%sproperties/%sminor.version' % (pom_version, pom_version)).text = new_minor_version

print ("Version has been changed in %s" % file)
#tree.write('%sresult.xml' % working_directory)
tree.write('%sresult.xml' % working_directory, default_namespace=xmlnamespace)
os.system("mv -f %sresult.xml %s" % (working_directory, file))
#os.system("git add %s" % file)
os.system("mv %srest/target/%s-%s %srest/target/ROOT.war" % (working_directory, git_branch, parent_app_version,
                                                             working_directory))
#os.system("git commit -m 'Update pom.xml files, current version is %s'" % new_app_version)


#print files

# for file in files:
#     os.system("rm -rf %sresult*.xml" % working_directory)
#     tree = et.parse(file)
#     root = tree.getroot()
#     xmlnamespace = root.tag.split('{')[1].split('}')[0]
#     try:
#         parent_app_version = root.find('%sversion' % pom_version).text
#     except AttributeError:
#         pass
#     major_version = parent_app_version.split('.')
#     minor_version = str(int(major_version[1].split('-')[0])+1)
#     new_app_version = str(major_version[0]) + '.' + str(minor_version) + '-SNAPSHOT'
#     try:
#         root.find('%sversion' % pom_version).text = new_app_version
#     except AttributeError:
#         root.find('%sparent/%sversion' % (pom_version, pom_version)).text = new_app_version
#     print ("Version has been changed in %s" % file)
#     tree.write('%sresult.xml' % working_directory)
#     tree.write('%sresult.xml' % working_directory, default_namespace=xmlnamespace)
#     os.system("mv -f %sresult.xml %s" % (working_directory, file))
#     os.system("git add %s" % file)
# os.system("mv %srest/target/%s-%s %srest/target/ROOT.war" % (working_directory, git_branch, parent_app_version,
#                                                              working_directory))
# os.system("git commit -m 'Update pom.xml files, current version is %s'" % new_app_version)