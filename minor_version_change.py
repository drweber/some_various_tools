#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import os
import subprocess
import sys

#OLD_VERSION=int(os.system("grep 'minor.version' ~/test.xml | awk -F'>' '{print $2}' | awk -F'<' '{print $1}'"))

def gitAdd(fileName, repoDir):
    cmd = 'git add ' + fileName
    pipe = subprocess.Popen(cmd, shell=True, cwd=repoDir,stdout = subprocess.PIPE,stderr = subprocess.PIPE )
    (out, error) = pipe.communicate()
    print out,error
    pipe.wait()
    return

def gitCommit(commitMessage, repoDir):
    cmd = 'git commit -am "%s"'%commitMessage
    pipe = subprocess.Popen(cmd, shell=True, cwd=repoDir,stdout = subprocess.PIPE,stderr = subprocess.PIPE )
    (out, error) = pipe.communicate()
    print out,error
    pipe.wait()
    return

files = []
working_directory = sys.argv[1]
app_name = sys.argv[2]
old_version = '999999999999999999999999999999'
new_version = 999999999999999999999999999999

files.append(os.path.join(working_directory, 'pom.xml'))
file = files[0]

file = '/Users/m_karytka/pom.xml'
file_tmp = '/Users/m_karytka/pom1.xml'
f1 = open('%s' % file, 'r')
f2 = open('%s' % file_tmp, 'w')
for line in f1:
    if '<minor.version>' in line:
        found = line
        old_version = found.split('>')[1].split('<')[0]
        new_version = int(old_version) + 1
    f2.write(line.replace('<minor.version>%s</minor.version>' % old_version,
                          '<minor.version>%s</minor.version>' % new_version))
f1.close()
f2.close()
os.rename('%s' % file_tmp, '%s' % file)
#os.system("git add %s" % file)