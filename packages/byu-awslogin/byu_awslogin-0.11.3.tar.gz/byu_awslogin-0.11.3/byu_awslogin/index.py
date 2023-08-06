#!/usr/bin/env python3

import configparser
import getpass
import click
import os
import sys
import datetime
import platform
from os.path import expanduser

from .consoleeffects import Colors

try:
    import lxml.etree as ET
except ImportError:
    if platform.system() == 'Windows':
        print('awslogin will not run on your machine yet.  Please follow the instructions at https://github.com/byu-oit/awslogin/releases/tag/lxml to get it running.')
        sys.exit(1)
    else:
        raise
from .adfs_auth import authenticate
from .assume_role import ask_which_role_to_assume, assume_role
from .roles import action_url_on_validation_success, retrieve_roles_page

__VERSION__ = '0.11.3'

# Enable VT Mode on windows terminal code from:
# https://bugs.python.org/issue29059
# This works not sure if it the best way or not
if platform.system().lower() == 'windows':
    from ctypes import windll, c_int, byref
    stdout_handle = windll.kernel32.GetStdHandle(c_int(-11))
    mode = c_int(0)
    windll.kernel32.GetConsoleMode(c_int(stdout_handle), byref(mode))
    mode = c_int(mode.value | 4)
    windll.kernel32.SetConsoleMode(c_int(stdout_handle), mode)


@click.command()
@click.version_option(version=__VERSION__)
@click.option('-a', '--account', help='Account to login with')
@click.option('-r', '--role', help='Role to use after login')
@click.option('-p', '--profile', default='default', help='Profile to use store credentials. Defaults to default')
@click.option('-s', '--status', is_flag=True, default=False, help='Display current logged in status. Use profile all to see all statuses')
def cli(account, role, profile, status):
    if not sys.version.startswith('3.6'):
        sys.stderr.write("{}byu_awslogin requires python 3.6{}\n".format(Colors.red, Colors.white))
        sys.exit(-1)
    if status:
        get_status(aws_file('config'), profile)
        return
    # Get the federated credentials from the user
    cached_netid = load_last_netid(aws_file('config'), profile)
    if cached_netid:
        net_id_prompt = 'BYU Net ID [{}{}{}]: '.format(Colors.blue,cached_netid,Colors.normal)
    else:
        net_id_prompt = 'BYU Net ID: '
    net_id = input(net_id_prompt) or cached_netid
    if "@byu.local" in net_id:
        print('{}@byu.local{} is not required'.format(Colors.lblue,Colors.normal))
        username = net_id
    else:
        username = '{}@byu.local'.format(net_id)
    password = getpass.getpass()
    print('')

    ####
    # Authenticate against ADFS with DUO MFA
    ####
    html_response, session, auth_signature, duo_request_signature = authenticate(username, password)

    # Overwrite and delete the credential variables, just for safety
    username = '##############################################'
    password = '##############################################'
    del username
    del password

    ####
    # Obtain the roles available to assume
    ####
    roles_page_url = action_url_on_validation_success(html_response)
    account_names, principal_roles, assertion, aws_session_duration = retrieve_roles_page(
        roles_page_url,
        html_response,
        session,
        auth_signature,
        duo_request_signature,
    )

    ####
    # Ask user which role to assume
    ####
    account_roles = ask_which_role_to_assume(account_names, principal_roles, account, role)

    ####
    # Assume roles and set in the environment
    ####
    for account_role in account_roles:
        aws_session_token = assume_role(account_role, assertion)

        # If assuming roles across all accounts, then use the account name as the profile name
        if account == 'all':
            profile = account_role.account_name

        check_for_aws_dir()
        write_to_cred_file(aws_file('creds'), aws_session_token, profile)
        write_to_config_file(aws_file('config'), net_id, 'us-west-2', profile, account_role.role_name, account_role.account_name)
    
        if account_role.role_name == "AccountAdministrator":
            print("Now logged into {}{}{}@{}{}{}".format(Colors.red,account_role.role_name, Colors.white, Colors.yellow,account_role.account_name,Colors.normal))
        else:
            print("Now logged into {}{}{}@{}{}{}".format(Colors.cyan,account_role.role_name, Colors.white, Colors.yellow,account_role.account_name,Colors.normal))


def aws_file(file_type):
    if file_type == 'creds':
        return "{}/.aws/credentials".format(expanduser('~'))
    else:
        return "{}/.aws/config".format(expanduser('~'))


def open_config_file(file):
    config = configparser.ConfigParser()
    config.read(file)
    return config


def check_for_aws_dir(directory="{}/.aws".format(expanduser('~'))):
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_to_cred_file(file, aws_session_token, profile):
    config = open_config_file(file)
    config[profile] = {
        'aws_access_key_id': aws_session_token['Credentials']['AccessKeyId'],
        'aws_secret_access_key': aws_session_token['Credentials']['SecretAccessKey'],
        'aws_session_token': aws_session_token['Credentials']['SessionToken']
    }
    with open(file, 'w') as configfile:
        config.write(configfile)


def write_to_config_file(file, net_id, region, profile, role, account):
    one_hour = datetime.timedelta(hours=1)
    expires = datetime.datetime.now() + one_hour
    config = open_config_file(file)
    config[profile] = {
        'region': region,
        'adfs_netid': net_id,
        'adfs_role': f'{role}@{account}',
        'adfs_expires': expires.strftime('%m-%d-%Y %H:%M')
    }
    with open(file, 'w') as configfile:
        config.write(configfile)


def load_last_netid(file, profile):
    config = open_config_file(file)
    if config.has_section(profile) and config.has_option(profile, 'adfs_netid'):
        return config[profile]['adfs_netid']
    else:
        return ''


def get_status_message(config, profile):
    if config.has_option(profile, 'adfs_role') and config.has_option(profile, 'adfs_expires'):
        expires = check_expired(config[profile]['adfs_expires'])
        account_name = f"{Colors.cyan}{config[profile]['adfs_role']}"
        if expires == 'Expired':
            expires_msg = f"{Colors.red}{expires} at: {config[profile]['adfs_expires']}"
        else:
            expires_msg = f"{Colors.yellow}{expires} at: {config[profile]['adfs_expires']}"
        return f"{account_name} {Colors.white}- {expires_msg}"
    else:
        return f"{Colors.red}Couldn't find status info"


def get_status(file, profile='default'):
    config = open_config_file(file)
    if profile == 'all':
        for x in config:
            if x == 'DEFAULT':
                continue
            message = get_status_message(config, x)
            print(f"{Colors.white}{x} - {message}")
        return
    else:
        if config.has_section(profile):
            message = get_status_message(config, profile)
            print(message)
        else:
            print(f"{Colors.red}Couldn't find profile: {profile}")
        return


def check_expired(expires):
    expires = datetime.datetime.strptime(expires, '%m-%d-%Y %H:%M')
    if expires > datetime.datetime.now():
        return 'Expires'
    else:
        return 'Expired'


if __name__ == '__main__':
    cli()
