import os
import unittest
from pyramid.testing import cleanUp
from pyramid.exceptions import ConfigurationError
from io import BytesIO
from tests.test_config import pkgs

class TestAssertBody(unittest.TestCase):

    def setUp(self):
        self.filename = 'test_assets.py'
        self.provider = self._makeOne(pkgs.asset)

    def test_assert_body_equal(self):
        resource_name = 'test_assets.py'
        result = self.provider.get_resource_string(None, resource_name)
        _assertBody(result, os.path.join(os.path.dirname(__file__), self.filename))

    def test_assert_body_with_different_line_endings(self):
        resource_name = 'test_assets_with_crlf.py'
        result = self.provider.get_resource_string(None, resource_name)
        _assertBody(result, os.path.join(os.path.dirname(__file__), self.filename))

    def test_assert_body_empty(self):
        resource_name = 'empty_file.py'
        result = self.provider.get_resource_string(None, resource_name)
        _assertBody(result, os.path.join(os.path.dirname(__file__), self.filename))

    def test_assert_body_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            _assertBody(b'some body', 'non_existent_file.py')

    def test_assert_body_mismatched_content(self):
        resource_name = 'mismatched_file.py'
        result = self.provider.get_resource_string(None, resource_name)
        with self.assertRaises(AssertionError):
            _assertBody(result, os.path.join(os.path.dirname(__file__), self.filename))

    def tearDown(self):
        cleanUp()