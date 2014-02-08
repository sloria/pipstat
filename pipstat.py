#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''pipstat
Prints download statistics for PyPI packages.

Usage:
    pipstat <package> ...
'''
from __future__ import unicode_literals, print_function
import sys
import math
from collections import OrderedDict

import xmlrpclib

__version__ = "0.1.0"
__author__ = "Steven Loria"
__license__ = "MIT"

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


def bargraph(data):
    """Return a bar graph as a string, given a dictionary of data."""
    lines = []
    max_length = min(max(len(key) for key in data.keys()), 20)
    n_val_characters = 80 - max_length
    max_val = max(data.values())
    max_val_length = max(len(str(val)) for val in data.values())
    scale = max(1, int(math.ceil(float(max_val) / n_val_characters)))
    template = "{key:{key_width}} [ {value:{val_width}d} ] {bar}"
    for key, value in data.items():
        bar = (value / scale) * TICK
        line = template.format(key=key[:max_length], value=value,
            bar=bar, key_width=max_length, val_width=max_val_length)
        lines.append(line)
    return '\n'.join(lines)


class Package(object):

    def __init__(self, name, client=None):
        self.client = client
        self.name = name

    @lazy_property
    def versions(self):
        """Return a list of versions"""
        return self.client.package_releases(self.name, True)

    @lazy_property
    def version_downloads(self):
        """Return a dictionary of version:download_count pairs."""
        ret = OrderedDict()
        for release in reversed(self.versions):
            downloads = self.client.release_downloads(self.name, release)
            download_count = sum(dl for _, dl in downloads)
            ret[release] = download_count
        return ret

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
        return 'Package(name={0:r})'.format(self.name)


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
        client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
        for name in package_names:
            print("Fetching statistics for {name!r}. . .".format(name=name))
            package = Package(name, client=client)
            graph = bargraph(package.version_downloads)
            min_ver, min_downloads = package.min_version
            max_ver, max_downloads = package.max_version
            avg_downloads = package.average_downloads
            total = package.downloads
            print()
            header = "Download statistics for {name}".format(name=name)
            print(header)
            print('=' * len(header))
            print()
            print(graph)
            print()
            print("Min downloads:\t\t{min_downloads:,} ({min_ver})".format(**locals()))
            print("Max downloads:\t\t{max_downloads:,} ({max_ver})".format(**locals()))
            print("Avg downloads:\t\t{avg_downloads:,}".format(**locals()))
            print("Total downloads:\t{total:,}".format(**locals()))
            print()
    sys.exit(0)

if __name__ == '__main__':
    main()
