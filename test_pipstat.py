# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from subprocess import check_output

from pipstat import Package

def test_package_releases(m_releases):
    pass

def run_cmd(cmd):
    '''Run a shell command `cmd` and return its output.'''
    return check_output(cmd, shell=True).decode('utf-8')
