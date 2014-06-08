# -*- coding: utf-8 -*-
import os

import requests
import responses
import pytest

import pipstat

HERE = os.path.abspath(os.path.dirname(__file__))

def setup_module():
    with open(os.path.join(HERE, 'response.json'), 'r') as fp:
        response_body = fp.read()
    responses.add(
        responses.GET,
        'http://pypi.python.org/pypi/webargs/json',
        body=response_body,
        content_type='application/json'
    )
    responses.add(
        responses.GET,
        'http://pypi.python.org/pypi/nope/json',
        status=404
    )
    responses.start()

def teardown_module():
    responses.stop()

@pytest.fixture
def package():
    return pipstat.Package('webargs')

class TestPackage:

    def test_versions(self, package):
        assert package.versions == [0.1]
