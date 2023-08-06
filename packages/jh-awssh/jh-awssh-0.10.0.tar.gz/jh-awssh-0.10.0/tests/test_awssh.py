#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `awssh` package."""

import pytest
import os
import boto3

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

    assh = awssh.Awssh()

    assert 'ec2 us-west-2' in assh.client('ec2')

    with pytest.raises(Exception):
        assh.client('false')

def test_return_ec2_servers(monkeypatch):

    awsh = awssh.Awssh()


def mock_describe_instances(monkeypatch):
    pass
