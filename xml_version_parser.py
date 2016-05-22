from xml.etree import ElementTree as et
import fnmatch
import os
import sys

files = []
working_directory = sys.argv[1]
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
        parent_pom_version = root.find('%sversion' % pom_version).text
        major_version = parent_pom_version.split('.')
        minor_version = str(int(major_version[1].split('-')[0])+1)
        root.find('%sversion' % pom_version).text = str(major_version[0]) + '.' + str(minor_version) + '-SNAPSHOT'
    except AttributeError:
        slave_pom_version = parent_pom_version
        #slave_pom_version = root.find('%sparent/%sversion' % (pom_version, pom_version)).text
        major_version = slave_pom_version.split('.')
        minor_version = str(int(major_version[1].split('-')[0])+1)
        root.find('%sparent/%sversion' % (pom_version, pom_version)).text = str(major_version[0]) + '.' + str(minor_version) + '-SNAPSHOT'
    print ("Version has changed in %s" % file)    
    tree.write('%sresult.xml' % working_directory)
    tree.write('%sresult.xml' % working_directory, default_namespace=xmlnamespace)
    os.system("mv -f %sresult.xml %s" % (working_directory, file))
