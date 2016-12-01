#!/usr/bin/env bash
#
## Simple IPTables Firewall with Whitelist & Blacklist
#
## List Locations
#

WHITELIST=/root/whitelist.txt
BLACKLIST=/root/blacklist.txt

#
## Specify where IP Tables is located
#

IPTABLES=/sbin/iptables
IPTABLES_SAVE=/sbin/iptables-save


DNS_NAMES="akamai.bintray.com jcenter.bintray.com maven.fabric.io fabric.io crashlytics.com repo.maven.apache.org google.com updates.jenkins-ci.org repo.us-west-1.amazonaws.com pkg.jenkins-ci.org ftp-chi.osuosl.org services.gradle.org downloads.gradle.org s3.amazonaws.com repo.jfrog.org fastdl.mongodb.org distribution-uploads.crashlytics.com services.gradle.org cm.crashlytics.com ec2-54-219-126-252.us-west-1.compute.amazonaws.com ec2-54-176-78-3.us-west-1.compute.amazonaws.com ec2-54-215-89-219.us-west-1.compute.amazonaws.com ec2-54-219-59-164.us-west-1.compute.amazonaws.com"
ALLOWED_PORTS="22 25 80 443 465 563 873 2200 8080 8081 9418 39066"

#
## Save current $IPTABLES running configuration in case we want to revert back
## To restore using our example we would run "/sbin/$IPTABLES-restore < /usr/src/$IPTABLES.last"
#

$IPTABLES_SAVE > /usr/local/etc/iptables.last

#
## Clear current rules
#

$IPTABLES -F
echo 'Clearing tables'
$IPTABLES -X
echo 'Deleting user defined chains'
$IPTABLES -Z
echo 'Zero chain counters'

rm -rf /root/whitelist.txt
touch /root/whitelist.txt

for NAME in $DNS_NAMES; do
dig +short $NAME | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" >> /root/whitelist.txt
done

#Always allow localhost.
echo 'Allowing Localhost'
$IPTABLES -A INPUT -s 127.0.0.1 -j ACCEPT

#
## Whitelist
#
for IP in `grep -v ^# $WHITELIST | awk '{print $1}'`; do
echo "Permitting IP: $IP"
$IPTABLES -A INPUT -s $IP -j ACCEPT
$IPTABLES -A OUTPUT -d $IP -j ACCEPT
done

#
## Blacklist
#
for x in `grep -v ^# $BLACKLIST | awk '{print $1}'`; do
echo "Denying IP: $x"
$IPTABLES -A INPUT -s $x -j DROP
done

#
## Permitted Ports
#
for PORT in $ALLOWED_PORTS; do
echo "Accepting port TCP $PORT"
$IPTABLES -A INPUT -p tcp --dport $PORT -j ACCEPT
$IPTABLES -A OUTPUT -p tcp --sport $PORT -j ACCEPT
echo "Accepting port UDP $PORT"
$IPTABLES -A INPUT -p udp --dport $PORT -j ACCEPT
$IPTABLES -A OUTPUT -p udp --sport $PORT -j ACCEPT
done

echo "Permitting Waverley Office IP 46.164.143.150"
$IPTABLES -I INPUT -s 46.164.143.150 -j ACCEPT
$IPTABLES -I OUTPUT -d 46.164.143.150 -j ACCEPT

#
## Limitation HTTP trafic
#
echo "HTTP Traffic restriction"
$IPTABLES -A INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
$IPTABLES -A OUTPUT -m limit --limit 100/minute --limit-burst 100 -j ACCEPT

#
## DNS ALLOW
#
echo "DNS Traffic Allow"
$IPTABLES -A OUTPUT -p udp --sport 1024:65535 --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
$IPTABLES -A INPUT -p udp  --sport 53 --dport 1024:65535 -m state --state ESTABLISHED -j ACCEPT
$IPTABLES -A OUTPUT -p tcp --sport 1024:65535 --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
$IPTABLES -A INPUT -p tcp --sport 53 --dport 1024:65535 -m state --state ESTABLISHED -j ACCEPT
$IPTABLES -A INPUT -p udp -s 0/0 --sport 1024:65535 --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
$IPTABLES -A OUTPUT -p udp --sport 53 -d 0/0 --dport 1024:65535 -m state --state ESTABLISHED -j ACCEPT
$IPTABLES -A INPUT -p udp -s 0/0 --sport 53 --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
$IPTABLES -A OUTPUT -p udp --sport 53 -d 0/0 --dport 53 -m state --state ESTABLISHED -j ACCEPT

#
## RESTRICTED ALL OTHER UDP PORTS
#
echo "All other UDP Ports INOUT & OUTPUT are restricted"
#$IPTABLES -A OUTPUT -p udp -j DROP
#$IPTABLES -A INPUT -p udp -j DROP
#$IPTABLES -A INPUT -p tcp --syn -j DROP
#$IPTABLES -A OUTPUT -p tcp --syn -j DROP
