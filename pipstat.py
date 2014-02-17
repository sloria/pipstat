#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''pipstat
Prints download statistics for PyPI packages.

Usage:
    pipstat <package> ...
'''
from __future__ import unicode_literals, print_function, division
import sys
import os
import time
PY2 = int(sys.version[0]) == 2
import math
from collections import OrderedDict
if PY2:
    from xmlrpclib import ServerProxy
else:
    from xmlrpc.client import ServerProxy

__version__ = "0.2.1"
__author__ = "Steven Loria"
__license__ = "MIT"

DATE_FORMAT = "%y/%m/%d"
MARGIN = 3
TICK = '*'


def lazy_property(fn):
    """Decorator that makes a property lazy-evaluated."""
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property


def get_display_width():
    """Get the maximum display width to output."""
    fallback = int(os.environ.get('COLUMNS', 80))
    try:  # On Python 3.3, we can use the entire width of the terminal
        return os.get_terminal_size().columns
    except (AttributeError, OSError):
        pass
    return fallback


def bargraph(data):
    """Return a bar graph as a string, given a dictionary of data."""
    lines = []
    max_length = min(max(len(key) for key in data.keys()), 20)
    max_val = max(data.values())
    max_val_length = max(len('{:,}'.format(val)) for val in data.values())
    max_bar_width = get_display_width() - (max_length + 3 + max_val_length + 3)
    template = "{key:{key_width}} [ {value:{val_width},d} ] {bar}"
    for key, value in data.items():
        try:
            bar = int(math.ceil(max_bar_width * value / max_val)) * TICK
        except ZeroDivisionError:
            bar = ''
        line = template.format(key=key[:max_length], value=value,
            bar=bar, key_width=max_length, val_width=max_val_length)
        lines.append(line)
    return '\n'.join(lines)


class NotFoundError(Exception):
    pass


class Package(object):

    def __init__(self, name, client):
        self.client = client
        self.name = name

    @lazy_property
    def versions(self):
        """Return a list of versions"""
        versions = self.client.package_releases(self.name, True)
        if versions:
            return versions
        else:
            raise NotFoundError('Package not found')

    @lazy_property
    def release_urls(self):
        return [self.client.release_urls(self.name, release)
                for release in self.versions]

    @lazy_property
    def version_downloads(self):
        """Return a dictionary of version:download_count pairs."""
        ret = OrderedDict()
        for release, info in self.release_info:
            download_count = sum(file_['downloads'] for file_ in info)
            ret[release] = download_count
        return ret

    @property
    def release_info(self):
        return reversed(list(zip(self.versions, self.release_urls)))

    @lazy_property
    def version_dates(self):
        ret = OrderedDict()
        for release, info in self.release_info:
            if info:
                upload_time = info[0]['upload_time']
                ret[release] = upload_time
        return ret

    def chart(self):
        data = OrderedDict()
        for version, dl_count in self.version_downloads.items():
            date = self.version_dates.get(version)
            date_formatted = ''
            if date:
                date_formatted = time.strftime(DATE_FORMAT,
                    self.version_dates[version].timetuple())
            key = "{0:7} {1}".format(version, date_formatted)
            data[key] = dl_count
        return bargraph(data)

    @lazy_property
    def downloads(self):
        """Total download count."""
        return sum(self.version_downloads.values())

    @lazy_property
    def max_version(self):
        """Version with the most downloads."""
        data = self.version_downloads
        return max(data.items(), key=lambda item: item[1])

    @lazy_property
    def min_version(self):
        """Version with the fewest downloads."""
        data = self.version_downloads
        return min(data.items(), key=lambda item: item[1])

    @lazy_property
    def average_downloads(self):
        """Average number of downloads."""
        return int(self.downloads / len(self.versions))

    def __repr__(self):
        return 'Package(name={0!r})'.format(self.name)


def create_server_proxy():
    return ServerProxy('http://pypi.python.org/pypi')


def main():
    """Main entry point for the pipstat CLI. Prints download stats to std out.
    """
    if '-h' in sys.argv or '--help' in sys.argv:
        print(__doc__)
        sys.exit(0)
    if '-v' in sys.argv or '--version' in sys.argv:
        print(__version__)
        sys.exit(0)
    package_names = sys.argv[1:]
    if len(package_names) < 1:
        print("No package names specified.")
        print(__doc__)
        sys.exit(1)
    else:
        client = create_server_proxy()
        for name in package_names:
            print("Fetching statistics for {name!r}. . .".format(name=name))
            package = Package(name, client=client)
            try:
                version_downloads = package.version_downloads
            except NotFoundError:
                print("No versions of {0!r} were found.".format(name))
                sys.exit(1)
            chart = package.chart()
            min_ver, min_downloads = package.min_version
            max_ver, max_downloads = package.max_version
            avg_downloads = package.average_downloads
            total = package.downloads
            print()
            header = "Download statistics for {name}".format(name=name)
            print(header)
            print('=' * len(header))
            print('Downloads by version')
            print(chart)
            print()
            print("Min downloads:   {min_downloads:12,} ({min_ver})".format(**locals()))
            print("Max downloads:   {max_downloads:12,} ({max_ver})".format(**locals()))
            print("Avg downloads:   {avg_downloads:12,}".format(**locals()))
            print("Total downloads: {total:12,}".format(**locals()))
            print()
    sys.exit(0)

if __name__ == '__main__':
    main()
