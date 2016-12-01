#!/bin/bash - 
#===============================================================================
#
#          FILE: install_web.sh
# 
#         USAGE: ./install_web.sh 
# 
#   DESCRIPTION: Auto deploy Matrixx Server
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: run under user with sudo rigths
#        AUTHOR: Mikalai Karytka, 
#  ORGANIZATION: 
#       CREATED: 08/31/16 14:48
#      REVISION: 0.6
#===============================================================================

set -o nounset                              # Treat unset variables as an error

echo "Set SELinux to permissive mode"
sudo setenforce Permissive

echo "Time to install Mongo"
MONGODB_VERSION="-3.2.9-1.el6.x86_64"
TOMCAT_VERSION="8.0.36"
MAVEN_VERSION="3.3.9"
MONGODB_INSTALL="mongodb-org-shell mongodb-org-tools mongodb-org-mongos mongodb-org-server mongodb-org"
baseurl=https://repo.mongodb.org/yum/redhat/6/mongodb-org/3.2/x86_64/RPMS/
for APP in $MONGODB_INSTALL;
do
echo "installing $APP"
if [ -f "/home/devops/$APP$MONGODB_VERSION.rpm" ]
then
  baseurl="/home/devops/"
fi
sudo yum install $baseurl$APP$MONGODB_VERSION.rpm -y
done

echo "Start MongoDB"
sudo service mongod start

echo "Check that MongoDB is started"
sudo grep "waiting for connections on port" /var/log/mongodb/mongod.log

echo "Ensure that MongoDB will start following a system reboot"
sudo chkconfig mongod on

echo "Check that Git is installed"
git --version || (echo "Installing Git" && sudo yum install git -y)

cd /opt/
echo "Installing Oracle Java"
sudo wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u45-b14/jdk-8u45-linux-x64.rpm"
sudo rpm -Uvh jdk-8u45-linux-x64.rpm
echo "Check that Java is installed"
java -version
javac -version

echo "Installing Tomcat"
sudo mkdir /opt/tomcat/ && cd /opt/tomcat
sudo wget http://apache.org/dist/tomcat/tomcat-8/v$TOMCAT_VERSION/bin/apache-tomcat-$TOMCAT_VERSION.zip
sudo unzip apache-tomcat-$TOMCAT_VERSION.zip
cd apache-tomcat-$TOMCAT_VERSION/bin
sudo chmod 700 /opt/tomcat/apache-tomcat-$TOMCAT_VERSION/bin/*.sh
sudo ln -s /opt/tomcat/apache-tomcat-$TOMCAT_VERSION/bin/startup.sh /usr/bin/tomcatup
sudo ln -s /opt/tomcat/apache-tomcat-$TOMCAT_VERSION/bin/shutdown.sh /usr/bin/tomcatdown
sudo tomcatup
echo "Wait until Tomcat is poweruped"
sleep 5
echo "Check that Tomcat is poweruped"
curl http://127.0.0.1:8080/

cd /opt/
echo "Installing Apache-Maven"
sudo wget http://apache.org/dist/maven/maven-3/$MAVEN_VERSION/binaries/apache-maven-$MAVEN_VERSION-bin.zip
sudo unzip apache-maven-$MAVEN_VERSION-bin.zip
export PATH=/opt/apache-maven-$MAVEN_VERSION/bin:$PATH

echo "Check Maven Path exported"
echo $PATH

echo "export PATH=/opt/apache-maven-$MAVEN_VERSION/bin:$PATH" >> ~/.bash_profile
echo "Check that Maven is installed"
mvn -v
