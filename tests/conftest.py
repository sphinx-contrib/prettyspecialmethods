"""
    pytest config for sphinxcontrib/prettyspecialmethods/tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2017 by Thomas Smith <Your email>
    :license: BSD, see LICENSE for details.
"""
import pytest
from sphinx.testing.path import path

pytest_plugins = ['sphinx.testing.fixtures']


@pytest.fixture(scope='session')
def rootdir():
    return path(__file__).parent.abspath()
