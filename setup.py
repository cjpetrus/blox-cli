from setuptools import setup
# you may need setuptools instead of distutils

setup(
    # basic stuff here
    scripts = [
        'bin/blox-cli',
        'bin/blox-create-environment.py',
        'bin/blox-create-deployment.py',
        'bin/blox-list-environments.py',
        'bin/blox-list-deployments.py',
        'bin/css-list-tasks.py',
        'bin/css-list-instances.py',
        'bin/list-task-definitions.py',
        'bin/register-task-definition.py',
        'bin/common.py',

    ]
)
