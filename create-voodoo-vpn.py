#!/usr/bin/env python
"""Creates an IPSec-over-L2TP VPN server on Amazon EC2.

This module creates a security group "voodoovpn" if necessary, creates
a new t1.micro instance, uses the shell script voodoo-vpn.sh to set it
up as a VPN server, and tags it with the name VoodooVPN. It thens
print out the host name of the server, the VPN username, and a
randomly generated Pre-Shared Key and VPN user password, for you to
use to configure your computer or devices.

Dependencies:
- the shell script voodoo-vpn.sh
- the external python module boto (installed globally via "sudo pip install boto")
- your AWS credentials, set in environmental variables, in ~/.boto, or in this script
- (optional) the name of an EC2 keypair for SSH access to the server

This module is known good with boto version=2.11.0 and AWS services as of 2013-09-02.

"""
import os
import random
import string
import re
import base64
import time
import sys

import boto
import boto.ec2


####################
# INPUT PARAMS
region_name='us-west-1'
# None, if no need to ssh into the box later
key_name = None
# None, if we want to get AWS creds from ~/.boto or environmental variables
aws_access_key_id=None
aws_secret_access_key=None

####################
# start

user_data_template_filename = 'voodoo-vpn.sh'
if not os.path.isfile(user_data_template_filename):
    exit(1)

# Canonical's AMI images for Ubuntu 12.04 LTS, as of 20130827
regionToAMIs = {"ap-northeast-1":"ami-b99b09b8",
                "ap-southeast-1":"ami-44135816",
                "ap-southeast-2":"ami-c526b4ff",
                "eu-west-1":"ami-1babb06f",
                "sa-east-1":"ami-c705a1da",
                "us-east-1":"ami-1b135e72",
                "us-west-1":"ami-1cf1db59",
                "us-west-2":"ami-f8ec70c8"}

image_id = regionToAMIs[region_name]

print(u"Connecting to EC2 in region %s" % region_name)
ec2 = boto.ec2.connect_to_region(region_name=region_name,
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)

print(u"Establishing security group voodoovpn")
voodoovpngroup_name = u'voodoovpn'
matching_security_groups = [sg for sg in ec2.get_all_security_groups() if sg.name==voodoovpngroup_name]
if len(matching_security_groups) > 0:
    print(u"Found security group voodoovpn")
    voodoovpngroup = matching_security_groups[0]
else:
    print(u"Creating security group voodoovpn")
    voodoovpngroup = ec2.create_security_group(voodoovpngroup_name,'Voodoo VPN access')
    voodoovpngroup.authorize('tcp',500,500,'0.0.0.0/0')
    voodoovpngroup.authorize('udp',500,500,'0.0.0.0/0')
    voodoovpngroup.authorize('udp',4500,4500,'0.0.0.0/0')
    if key_name is not None:
        # open an ssh port, if we provided an ssh key
        voodoovpngroup.authorize('tcp',22,22,'0.0.0.0/0')
        voodoovpngroup.authorize('udp',22,22,'0.0.0.0/0')
        

print(u"Generating VPN credentials")
# generate IPSEC_PSK, 
VPN_USER = 'voodoouser'
IPSEC_PSK = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits ) for x in range(32))
VPN_PASSWORD = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits ) for x in range(32))

print(u"Constructing script to configure EC2 VPN instance")
# for AWS, generate one-time user-data script
with open(user_data_template_filename) as f:
    user_data_template = f.read()

user_data = user_data_template
user_data = re.sub(r'VPN_USER=.*\n','VPN_USER="' + VPN_USER + '"\n',user_data)
user_data = re.sub(r'IPSEC_PSK=.*\n','IPSEC_PSK="' + IPSEC_PSK + '"\n',user_data)
user_data = re.sub(r'VPN_PASSWORD=.*\n','VPN_PASSWORD="' + VPN_PASSWORD + '"\n',user_data)

sys.stdout.write(u"Creating EC2 instance")
# on AWS, create the instance
reservation = ec2.run_instances(image_id=image_id,
                                key_name=key_name,
                                instance_type='t1.micro',
                                security_groups=[voodoovpngroup_name],
                                user_data=user_data)

instance = reservation.instances[0]

# Check up on its status every so often
status = instance.update()
while status == 'pending':
    time.sleep(1)
    sys.stdout.write('.')
    sys.stdout.flush()
    status = instance.update()
print(u".")

if status != 'running':
    print('Instance ' + instance.id + ' never reached status "running". Instance status: ' + status)
    exit(1)

print(u"Tagging instance")
ec2.create_tags([instance.id],{"Name": "VoodooVPN"})

print(u"VPN instance created and now running")

results = {"region_name":region_name,
           "instance_id":instance.id,
           "public_dns_name":instance.public_dns_name,
           "securitygroup_id":voodoovpngroup.id,
           "IPSEC_PSK":IPSEC_PSK,
           "VPN_USER":VPN_USER,
           "VPN_PASSWORD":VPN_PASSWORD}

print(results)

# return region_name, instance id, PSK, user/pass creds

# add VPN settings on the mac
# https://gist.github.com/kebot/5517680
