# -*- coding: utf-8 -*-

"""Console script for awssh."""

import click
import awssh
import subprocess
from termcolor import colored


@click.group(help="Helper to SSH into instances and list ips for mussh")
def main():
    """ Entry Point """
    pass


@main.command(help='List IPS for all instances and mark EIPs')
@click.option("--region", "-r",
              help="AWS Region, overrides ENV and shared config")
def ls(region=None):

    awsh = awssh.Awssh(region=region)
    servers = awsh.return_server_list()

    if len(servers) <= 0:
        click.echo("No ec2 instances found")
        return

    click.echo('-------------------------')
    click.echo('\t{0} = EIP'.format(colored('✓', 'green')))
    click.echo('-------------------------')

    for k, v in enumerate(servers):
        click.echo(
            '{0} [{1}]: {2}'.format(
                colored(
                    v['Eip'],
                    'green'),
                v['Ip'],
                v['Name']))


@main.command(help="List ip's for use with mussh. Fuzzy search enabled by default")
@click.option("--region", "-r",
              help="AWS Region, overrides ENV and shared config")
@click.option("--exact", "-e", is_flag=True, default=False,
              help='Disable fuzzy search and return exact Tag[Name] matches')
@click.argument('name')
def ips(name, region=None, exact=False):
    awsh = awssh.Awssh(region=region)
    ips = awsh.list_ips(name, exact=exact)
    if len(ips) <= 0:
        return

    for ip in ips:
        click.echo(ip)


@main.command(help='SSH Into instances')
@click.option("--user", "-u", default='ec2-user', help='SSH User')
@click.option(
    "--tty",
    "-t",
    default=False,
    is_flag=True,
    help="TTY SSH Option")
@click.option("--region", "-r",
              help="AWS Region, overrides ENV and shared config")
def ssh(user, tty, region=None):
    awsh = awssh.Awssh(region=region)
    servers = awsh.return_server_list()

    if len(servers) <= 0:
        click.echo("No servers available")
        return

    click.echo('-------------------------')
    click.echo('\t{0} = EIP'.format(colored('✓', 'green')))
    click.echo('-------------------------')

    for k, v in enumerate(servers):
        idx = k + 1
        if idx < 10:
            idx = ' {0}'.format(idx)

        click.echo(
            '{0}) {1} [{2}]: {3}'.format(
                idx,
                colored(
                    v['Eip'],
                    'green'),
                v['Ip'],
                v['Name']))

    prompt = 'Select a server to ssh into [1-{0}]'.format(len(servers))

    ans = click.prompt(prompt, type=int)

    if ans <= 0 or ans > len(servers):
        click.echo("Invalid selection")
        return

    if ans > 0 and ans <= len(servers):
        server = servers[(ans - 1)]
        if tty:
            tty = "-t"
        else:
            tty = ""
        click.echo("---------------------")
        click.echo(
            "Server: {0}({1})".format(
                server['Name'],
                server['Ip'].strip()))
        click.echo("User: {0}".format(user))
        click.echo("---------------------")
        subprocess.call(
            'ssh {2} {0}@{1}'.format(
                user,
                server['Ip'].strip(),
                tty),
            shell=True)


if __name__ == "__main__":
    main()
