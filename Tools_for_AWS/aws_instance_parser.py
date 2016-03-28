#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import sys
import json
import subprocess
from optparse import OptionParser

################################
# Initital config
################################
AIP_VERSION = "0.2.1"

# Эти данные понадобятся, для ввода с клавиатуры в качестве параметров
# AWS_SECRET_ACCESS_KEY = '@@@@@@@@@@'
# AWS_ACCESS_KEY_ID = '@@@@@@@@@@@@'
# AWS_DEFAULT_REGION = 'us-east-1'


def parse_commandline():
    ################################
    # Config OptionParser
    #####################r###########
    parser = OptionParser()
    availible_types = [
        'brief', 'short', 'full'
    ]
    availible_regions = [
        'us-east-1', 'us-west-1', 'us-west-2', 'eu-west-1', 'eu-central-1',
        'ap-northeast-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'sa-east-1'
    ]
    parser.add_option('-v', '--version', dest='version', action='store_true')
    parser.add_option('-k', '--aws-secret-access-key', dest='secret_key', help="AWS_SECRET_ACCESS_KEY")
    parser.add_option('-i', '--aws-access-key-id', dest='key_id', help="AWS_ACCESS_KEY_ID")
    parser.add_option('-r', '--aws-default-region', dest='region',
                      help='Please specify AWS_DEFAULT_REGION. Availible regions:' '{0}'.format(availible_regions))
    parser.add_option('', '--view_type', dest='view_type',
                      help='Availible types output informations:' '{0}'.format(availible_types))

    (options, args) = parser.parse_args()

    if options.version is True:
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
    if not options.view_type:
        options.view_type = 'full'
    elif options.view_type not in availible_types:
        parser.error('Please enter correct output type,' '{0}'.format(availible_types))
        parser.print_help()
    return options

def coloring(string, color):
    COLORS = {
        'reset': "\x1b[0m",
        'green': "\x1b[32;01m",
        'red': "\x1b[31;01m",
        'white': "\x1b[37;01m",
        'light_cyan': "\x1b[36;01m",
        'yellow': "\x1b[33;01m",
        'light_gray': "\x1b[37;01m",
        'blue': "\x1b[34;01m",
    }
    if color not in COLORS:
        color = 'reset'
    return '{0}{1}{2}'.format(COLORS[color], string, COLORS['reset'])

def is_json(myjson):
  try:
    json.loads(myjson)
  except (ValueError, KeyError, TypeError):
    return False
  return True

def output_parcer(aws_output,view_type):
    pass

def main_run():
    options = parse_commandline()
    AWS_SECRET_ACCESS_KEY = options.secret_key
    AWS_ACCESS_KEY_ID = options.key_id
    AWS_DEFAULT_REGION = options.region
    AWS_DEFAULT_OUTPUT = 'json'
    awsCmd = "aws ec2 describe-instances --output %s --region %s" % (AWS_DEFAULT_OUTPUT, AWS_DEFAULT_REGION)
    exportID = "export AWS_ACCESS_KEY_ID=%s" % AWS_ACCESS_KEY_ID
    exportKEY = "AWS_SECRET_ACCESS_KEY=%s" % AWS_SECRET_ACCESS_KEY
    subprocess.check_output(['bash','-c', exportID])
    subprocess.check_output(['bash','-c', exportKEY])
    output = subprocess.check_output(['bash','-c', awsCmd])
    if is_json(output):
        return output_parcer(output,options.view_type)
    else:
        print coloring('Information from Amazon AWS is not in JSON format','red')
        print coloring('\nAnswer from Amazon AWS is:', 'green')
        print coloring('%s','yellow') % output

if __name__ == '__main__':
    main_run()
