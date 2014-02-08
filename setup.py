import sys
import os
import subprocess

from setuptools import setup

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
    version="0.1.0",
    description='Get download counts for PyPI packages',
    long_description=read("README.rst"),
    author='Steven Loria',
    author_email='sloria1@gmail.com',
    url='https://github.com/sloria/pipstat',
    install_requires=['docopt'],
    license=read("LICENSE"),
    zip_safe=False,
    keywords='pipstat',
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
