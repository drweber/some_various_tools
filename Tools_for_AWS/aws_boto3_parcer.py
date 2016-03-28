#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import sys
import json
import collections
from optparse import OptionParser
try:
    import boto3
    from boto3.session import Session
except ImportError:
    sys.exit('Please install boto3 to continue "pip install boto3"')

################################
# Initital config
################################
AIP_VERSION = "0.3.0"


def parse_commandline():
    ################################
    # Config OptionParser
    #####################r###########
    parser = OptionParser()
    availible_regions = [
        'us-east-1', 'us-west-1', 'us-west-2', 'eu-west-1', 'eu-central-1',
        'ap-northeast-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'sa-east-1'
    ]
    parser.add_option('-v', '--version', dest='version', action='store_true')
    parser.add_option('-k', '--aws-secret-access-key', dest='secret_key', help="AWS_SECRET_ACCESS_KEY")
    parser.add_option('-i', '--aws-access-key-id', dest='key_id', help="AWS_ACCESS_KEY_ID")
    parser.add_option('-r', '--aws-default-region', dest='region',
                      help='Please specify AWS_DEFAULT_REGION. Availible regions:' '{0}'.format(availible_regions))

    (options, args) = parser.parse_args()

    if options.version:
        print "aip-{0}".format(AIP_VERSION)
    if not any(options.__dict__.values()):
        parser.print_help()
        sys.exit(0)
    elif not options.secret_key:
        parser.error('AWS_SECRET_ACCESS_KEY not defined')
        parser.print_help()
    elif not options.key_id:
        parser.error('AWS_ACCESS_KEY_ID not defined')
        parser.print_help()
    elif options.region not in availible_regions:
        parser.error('Please enter correct AWS_DEFAULT_REGION,' '{0}'.format(availible_regions))
        parser.print_help()
    return options


def get_session(type):
    options = parse_commandline()
    s = boto3.session.Session()
    session = s.resource(type,aws_access_key_id=options.key_id,
                  aws_secret_access_key=options.secret_key,
                  region_name=options.region)
    return session

def ls():
    ec2 = get_session('ec2')
    result = collections.OrderedDict()
    for instance in ec2.instances.all():
        ip_private = []
        ip_public = []
        for interface in instance.network_interfaces_attribute:
            try:
                for ip in interface['PrivateIpAddresses']:
                    ip_private.append(ip['PrivateIpAddress'])
                    try:
                        ip_public.append(ip['Association']['PublicIp'])
                    except KeyError:
                        ip_public = ['No']
            except KeyError:
                ip_private = ['No']
            instance_state = instance.state['Name']
            instance_state_reason = instance.state_reason['Message']
        result[instance.id] = {
            'Public Name':instance.public_dns_name,
            'IPs':{'Public':ip_public,'Private':ip_private},
            'State':instance_state,
            'StateReason':instance_state_reason,
            'Key':instance.key_name
        }
    return json.dumps(result,ensure_ascii=False)


def main():
    print ls()

if __name__ == '__main__':
    main()