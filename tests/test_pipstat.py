# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from subprocess import check_output, CalledProcessError
import pytest
import random
from datetime import datetime

import pipstat

random.seed(42)

# Build up a dict of release numbers => download counts
MOCK_PACKAGE = 'cheesetest'
versions = ['0.1', '0.1.1', '0.1.12', '0.2.0']
release_downloads = {}
release_urls = {}
for i, ver in enumerate(versions):
    tar = '{0}-{1}.tar.gz'.format(MOCK_PACKAGE, ver)
    whl = '{0}-{1}-py2.py3-none-any.whl'.format(MOCK_PACKAGE, ver)
    tar_downloads =  random.randint(0, 12345)
    whl_downloads = random.randint(0, 12345)
    release_downloads[ver] = [[tar, tar_downloads], [whl, whl_downloads]]
    release_urls[ver] = [
        {'downloads': tar_downloads, 'upload_date': datetime(2014, 5, i + 1)},
        {'downloads': whl_downloads, 'upload_date': datetime(2014, 5, i + 1)}
    ]


class MockClient(object):
    """A simple mock for xmlrpclib.ServerProxy."""

    def package_releases(self, name, hidden=False):
        if name == MOCK_PACKAGE and hidden:
            return ['0.1', '0.1.1', '0.1.12', '0.2.0']
        else:
            return []

    def release_downloads(self, name, version):
        if name == MOCK_PACKAGE:
            return release_downloads[version]
        else:
            return []

    def release_urls(self, name, version):
        if name == MOCK_PACKAGE:
            return release_urls[version]
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


def test_repr(package):
    assert repr(package) == 'Package(name={0!r})'.format(MOCK_PACKAGE)


def test_version_downloads(package):
    for ver in package.versions:
        expected = sum(dl for _, dl in release_downloads[ver])
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
    avg = package.downloads / len(release_urls.keys())
    assert package.average_downloads == int(avg)


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
