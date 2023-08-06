'''
Module for utility functions
'''

import collections
from copy import deepcopy
from fabric.api import run as _run, hide
from fabric.colors import red, green, yellow


def halt(msg):
    ''' Terminate the script execution with a message '''
    raise SystemExit(red(msg))


def info(msg):
    ''' Print a message (Information) '''
    print('\n' + green(msg))


def remote_print(msg):
    ''' Print a raw message on the remote logs. '''
    with hide('running'):
        _run('echo "{}"'.format(msg))


def remote_info(msg):
    ''' Print a message (Information) on the remote logs. '''
    remote_print(green(msg))


def warn(msg):
    ''' Print a warning message. '''
    print('\n' + yellow(msg))


def warn_deprecated(msg):
    ''' Print a deprecated warning message. '''
    warn('Deprecated: {}'.format(msg))


def merge(dict1, dict2):
    ''' Merge Two dictionaries recursively. '''
    result = deepcopy(dict1)

    for key, value in dict2.iteritems():
        if isinstance(value, collections.Mapping):
            result[key] = merge(result.get(key, {}), value)
        else:
            result[key] = deepcopy(dict2[key])

    return result
