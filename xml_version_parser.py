from xml.etree import ElementTree as et
import fnmatch
import os

files = []
working_directory = 'path_to_working_dir'
pom_version = '{http://maven.apache.org/POM/4.0.0}'

for root1, dirnames, filenames in os.walk(working_directory):
    for filename in fnmatch.filter(filenames, 'pom.xml'):
        files.append(os.path.join(root1, filename))
for file in files:
    os.system("rm -rf %sresult*.xml" % working_directory)
    tree = et.parse(file)
    root = tree.getroot()
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
    os.system("sed -e 's/ns0://g;s/:ns0//g' %sresult.xml > %sresult2.xml" % (working_directory, working_directory))
    os.system("mv -f %sresult2.xml %s" % (working_directory, file))
