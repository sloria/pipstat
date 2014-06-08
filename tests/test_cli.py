# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from subprocess import check_output, CalledProcessError
import pytest

import pipstat


def test_pipstat_cmd_without_args_exits_with_nonzero_code():
    with pytest.raises(CalledProcessError):
        run_cmd('pipstat')


def test_pipstat_cmd_version():
    assert run_cmd('pipstat -v') == pipstat.__version__ + '\n'
    assert run_cmd('pipstat --version') == pipstat.__version__ + '\n'


def test_no_division_by_zero_in_bargraph():
    assert pipstat.TICK not in pipstat.bargraph({'foo': 0})


def run_cmd(cmd):
    '''Run a shell command `cmd` and return its output.'''
    return check_output(cmd, shell=True).decode('utf-8')
