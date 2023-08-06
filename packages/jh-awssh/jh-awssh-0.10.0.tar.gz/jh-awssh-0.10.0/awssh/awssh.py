# -*- coding: utf-8 -*-

import boto3
import os
import jmespath

"""Main module."""


class Awssh(object):

    _clients = {}
    _default_region = 'us-west-2'
    _region = None

    def __init__(self, region=None):

        if region:
            Awssh._region = region
        else:
            Awssh._region = Awssh.default_region()

    @staticmethod
    def client(service):

        if not Awssh._clients.get(service):

            client = boto3.client(service, region_name=Awssh.get_region()) or False  # noqa

            if not client:
                raise Exception(
                    'Could not create service: {0}'.format(service))

            Awssh._clients.update({service: client})

        return Awssh._clients.get(service)

    @staticmethod
    def default_region():

        if os.environ.get("AWS_DEFAULT_REGION") is not None:
            return os.environ.get("AWS_DEFAULT_REGION")

        return Awssh._default_region

    @staticmethod
    def get_region():
        return Awssh._region

    def return_ec2_servers(self, **kwargs):

        ec2Client = Awssh.client('ec2')

        inst = ec2Client.describe_instances()

        ips = []

        # compile JMESpath queries
        jmespath.compile("Tags[?Key=='Name'].Value")
        jmespath.compile("PublicIpAddress")
        jmespath.compile("PrivateIpAddress")

        for i in inst['Reservations']:
            for ii in i['Instances']:
                if ii['State']['Code'] not in [16]:
                    continue
                name = (jmespath.search("Tags[?Key=='Name'].Value", ii)[0]
                        or 'N/A')
                ip = jmespath.search("PublicIpAddress", ii) or False

                if ip:
                    ips.append({'Name': name, 'Ip': ip})

        return ips

    def return_elastic_ips(self, **kwargs):

        ec2Client = Awssh.client('ec2')

        ips = []

        eips = ec2Client.describe_addresses()

        for ip in eips['Addresses']:
            if 'PublicIp' in ip:
                ips.append(ip['PublicIp'])

        return ips

    def return_server_list(self, **kwargs):

        servers = self.return_ec2_servers()
        eips = self.return_elastic_ips()

        for k, v in enumerate(servers):
            tag = ' '
            if v['Ip'] in eips:
                tag = '✓'
            # pad the ips for uniformity
            while len(servers[k]['Ip']) < 15:
                servers[k]['Ip'] = ' {0}'.format(v['Ip'])
            servers[k].update({'Eip': tag})

        def cmp(x, y):
            if x['Name'] < y['Name']:
                return -1
            return 0

        servers = sorted(servers, cmp=cmp)

        return servers

    def list_ips(self, name, **kwargs):

        exact = False

        if kwargs.get('exact'):
            exact = kwargs['exact']

        servers = self.return_ec2_servers()

        ips = []

        if len(servers) <= 0:
            return ips

        name = name.lower()

        for k, v in enumerate(servers):
            if len(name) > 0:
                if exact:
                    if name == v['Name'].lower():
                        ips.append(v['Ip'])
                else:
                    if name in v['Name'].lower():
                        ips.append(v['Ip'])
            else:
                ips.append(v['Ip'])

        return ips
