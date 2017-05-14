#!/usr/bin/env python
import json, os, sys
from subprocess import Popen, PIPE
import ConfigParser
import subprocess

STRIP = [
    'AWS_ACCESS_KEY',
    'AWS_ACCESS_KEY_ID',
    'AWS_CONFIG_FILE',
    'AWS_DEFAULT_PROFILE',
    'AWS_DEFAULT_REGION',
    'AWS_PROFILE',
    'AWS_SECRET_ACCESS_KEY',
    'AWS_SECRET_KEY',
    'AWS_SESSION_TOKEN',
    'EC2_URL',
]
BLOX_COMMANDS = {'create-deployment': 'blox-create-deployment.py',
                 'create-environment': 'blox-create-environment.py',
                 'increment-cluster': 'increment-cluster-instances.py',
                 'list-deployments': 'blox-list-deployments.py',
                 'list-environments': 'blox-list-environments.py',
                 'list-tasks': 'css-list-tasks.py',
                 'list-instances': 'css-list-instances.py',
                 }


def load_aws_config(profile="blox"):
    environ = os.environ
    home = environ['HOME']
    aws_config = load_raw_config(os.path.join(home, '.aws', 'config'), region='us-west-2')
    aws_credentials = load_raw_config(os.path.join(home, '.aws', 'credentials'))
    return dict(
        region=aws_config.get('profile %s' % profile, 'region'),
        aws_access_key_id=aws_credentials.get(profile, 'aws_access_key_id'),
        aws_secret_access_key=aws_credentials.get(profile, 'aws_secret_access_key')
    )


def load_raw_config(path, **defaults):
    config = ConfigParser.RawConfigParser(defaults)
    config.read(path)
    return config


def run_command(command=None):
    os.system(' '.join(command))


def get_deployment_id(stack_name='BloxAws'):
    creds = load_aws_config('blox')
    proc = subprocess.Popen([
        "aws --region {} cloudformation describe-stack-resource --stack-name {} --logical-resource-id RestApi --query 'StackResourceDetail.PhysicalResourceId' --output text".format(
            creds.get('region'), stack_name)], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out


def main(*args, **kwargs):
    try:
        action = sys.argv[1]
    except:
        print """\n     Available Commands:\n          """ + "        \n          ".join(BLOX_COMMANDS.keys())
        return False
    creds = load_aws_config('blox')
    script_dir = os.path.realpath(os.path.dirname(sys.argv[0])) + "/"
    exec_command = ['python']
    if action in BLOX_COMMANDS.keys():
        exec_command += [script_dir + BLOX_COMMANDS[action]]
        exec_command += sys.argv[2:]
        run_command(exec_command)
    else:
        print """\n     Available Commands:\n          """ + "        \n          ".join(BLOX_COMMANDS.keys())
        return False

if __name__ == "__main__":
    deployment_id = get_deployment_id().strip().replace(" ", "")
    main(sys.argv, profile='blox')

