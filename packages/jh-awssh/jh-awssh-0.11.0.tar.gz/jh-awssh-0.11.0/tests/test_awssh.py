#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `awssh` package."""

import pytest
import os
import boto3
import json
import sys

from click.testing import CliRunner

from awssh import awssh

@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    # runner = CliRunner()
    # result = runner.invoke(awssh.cli.main)
    # assert result.exit_code == 0
    # # assert 'awssh.cli.main' in result.output
    # help_result = runner.invoke(awssh.cli.main, ['--help'])
    # assert help_result.exit_code == 0
    # assert '--help' in help_result.output


def test_awssh_default_region():

    os.environ['AWS_DEFAULT_REGION'] = 'us-test-1'

    assert 'us-test-1' in awssh.Awssh.default_region()

    ash = awssh.Awssh(region='us-test-2')

    assert 'us-test-2' in awssh.Awssh.get_region()

    del os.environ['AWS_DEFAULT_REGION']

    ash = awssh.Awssh()

    assert 'us-west-2' in ash.get_region()


def test_awssh_client(monkeypatch):

    def boto_client(service, **kwargs):
        if service == 'false':
            return False
        return '{0} {1}'.format(service, kwargs['region_name'])

    monkeypatch.setattr(boto3, 'client', boto_client)


    assert 'ec2 us-west-2' in awssh.Awssh.client('ec2')

    with pytest.raises(Exception):
        assh.client('false')

    monkeypatch.undo()
    awssh.Awssh._clients = {}

    def boto_client(service, **kwargs):
        raise Exception("UNABLE TO CONNECT")

    monkeypatch.setattr(boto3, 'client', boto_client)

    with pytest.raises(SystemExit):
        client = awssh.Awssh.client("ec2")


def test_return_ec2_servers_exception(monkeypatch):

    mock_describe_instances(monkeypatch)
    awsh = awssh.Awssh()

    servers = awsh.return_ec2_servers()

    servers_json = json.dumps(servers)

    assert '3.3.3.3' in servers_json
    assert '5.5.5.5' not in servers_json

    monkeypatch.undo()
    awssh.Awssh._clients = {}

    mock_describe_instances(monkeypatch)

    awsh.return_ec2_servers()
    print(sys.stdout)

def mock_describe_instances(monkeypatch):

    class ec2_mock():

        def __init__(self, name):
            self.name = name

        def describe_instances(self):
            return {
                'Reservations': [
                        {'Instances': [
                            {
                                'State': {'Code': 16},
                                'Tags': [
                                    {'Key': 'Name', 'Value': 'server1'},
                                    {'Key': 'NotName', 'Value': 'Bunk'},
                                ],
                                'PublicIpAddress': '0.0.0.0',
                                'PrivateIpAddress': '1.1.1.1',
                            },
                            {
                                'State': {'Code': 16},
                                'Tags': [
                                    {'Key': 'Name', 'Value': 'server2'},
                                    {'Key': 'NotName', 'Value': 'Bunk'},
                                ],
                                'PublicIpAddress': '3.3.3.3',
                                'PrivateIpAddress': '4.4.4.4',
                            }
                        ]
                    },
                    {'Instances': [
                            {
                                'State': {'Code': 3},
                                'Tags': [
                                    {'Key': 'Name', 'Value': 'server3'},
                                    {'Key': 'NotName', 'Value': 'Bunk'},
                                ],
                                'PublicIpAddress': '5.5.5.5',
                                'PrivateIpAddress': '6.6.6.6',
                            },
                            {
                                'State': {'Code': 16},
                                'Tags': [
                                    {'Key': 'Name', 'Value': 'server4'},
                                    {'Key': 'NotName', 'Value': 'Bunk'},
                                ],
                                'PublicIpAddress': '7.7.7.7',
                                'PrivateIpAddress': '8.8.8.8',
                            }
                        ]
                    }
                ]
            }

    def boto_client_mock(service, **kwargs):
        return ec2_mock(service)

    monkeypatch.setattr(boto3, 'client', boto_client_mock)

def mock_describe_instances_exception(monkeypatch):

    class ec2_mock():

        def __init__(self, name):
            self.name = name

        def describe_instances(self):
            raise Exception("Connection Error")


    def boto_client_mock(service, **kwargs):
        return ec2_mock(service)

    monkeypatch.setattr(boto3, 'client', boto_client_mock)
