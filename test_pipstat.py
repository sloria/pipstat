# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from subprocess import check_output, CalledProcessError
import pytest
import random

import pipstat

random.seed(42)

# Build up a dict of release numbers => download counts
MOCK_PACKAGE = 'cheesetest'
versions = ['0.1', '0.1.1', '0.1.12', '0.2.0']
releases = {}
for ver in versions:
    tar = '{0}-{1}.tar.gz'.format(MOCK_PACKAGE, ver)
    whl = '{0}-{1}-py2.py3-none-any.whl'.format(MOCK_PACKAGE, ver)
    releases[ver] = [[tar, random.randint(0, 12345)], [whl, random.randint(0, 12345)]]


class MockClient(object):
    """A simple mock for xmlrpclib.ServerProxy."""

    def package_releases(self, name, hidden=False):
        if name == MOCK_PACKAGE and hidden:
            return ['0.1', '0.1.1', '0.1.12', '0.2.0']
        else:
            return []

    def release_downloads(self, name, version):
        if name == MOCK_PACKAGE:
            return releases[version]
        else:
            return []


@pytest.fixture
def package():
    return pipstat.Package(MOCK_PACKAGE, client=MockClient())


def test_versions(package):
    assert package.versions == package.client.package_releases(MOCK_PACKAGE, True)


def test_error_raised_if_no_versions():
    p = pipstat.Package('notfound', client=MockClient())
    with pytest.raises(pipstat.NotFoundError):
        p.versions


def test_version_downloads(package):
    for ver in package.versions:
        expected = sum(dl for _, dl in releases[ver])
        assert package.version_downloads[ver] == expected


def test_downloads(package):
    assert package.downloads == sum(package.version_downloads.values())


def test_max_version(package):
    assert package.max_version == max(package.version_downloads.items(),
                                        key=lambda item: item[1])


def test_min_version(package):
    assert package.min_version == min(package.version_downloads.items(),
                                        key=lambda item: item[1])


def test_avg_downloads(package):
    avg = package.downloads / len(releases.keys())
    assert package.average_downloads == int(avg)


def test_pipstat_cmd_without_args_exits_with_nonzero_code():
    with pytest.raises(CalledProcessError):
        run_cmd('pipstat')


def test_pipstat_cmd_version():
    assert run_cmd('pipstat -v') == pipstat.__version__ + '\n'
    assert run_cmd('pipstat --version') == pipstat.__version__ + '\n'


def run_cmd(cmd):
    '''Run a shell command `cmd` and return its output.'''
    return check_output(cmd, shell=True).decode('utf-8')
