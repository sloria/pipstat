import sys
import re
import subprocess

from setuptools import setup


def find_version(fname):
    '''Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    '''
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version

__version__ = find_version("pipstat.py")

PUBLISH_CMD = "python setup.py register sdist upload"
TEST_PUBLISH_CMD = 'python setup.py register -r test sdist upload -r test'
TEST_CMD = 'nosetests'

if 'publish' in sys.argv:
    status = subprocess.call(PUBLISH_CMD, shell=True)
    sys.exit(status)

if 'publish_test' in sys.argv:
    status = subprocess.call(TEST_PUBLISH_CMD, shell=True)
    sys.exit()

def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    name='pipstat',
    version=__version__,
    description='Get download counts for PyPI packages from the command line',
    long_description=read("README.rst"),
    author='Steven Loria',
    author_email='sloria1@gmail.com',
    url='https://github.com/sloria/pipstat',
    install_requires=[],
    license=read("LICENSE"),
    zip_safe=False,
    keywords='pipstat pypi statistics download count metrics',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    py_modules=["pipstat"],
    entry_points={
        'console_scripts': [
            "pipstat = pipstat:main"
        ]
    },
    tests_require=['pytest'],
)
