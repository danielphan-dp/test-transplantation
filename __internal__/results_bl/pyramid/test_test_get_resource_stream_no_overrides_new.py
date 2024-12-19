import os
import unittest
from pyramid.testing import cleanUp
from pyramid.exceptions import ConfigurationError
from io import BytesIO
from tests.test_config import pkgs

class TestAssertBody(unittest.TestCase):

    def setUp(self):
        self.filename = 'test_assets.py'
        self.valid_body = b'This is a test body.'
        self.invalid_body = b'This is an invalid body.'
        self.empty_body = b''

    def test_assert_body_valid(self):
        with open(self.filename, 'wb') as f:
            f.write(self.valid_body)
        _assertBody(self.valid_body, self.filename)

    def test_assert_body_invalid(self):
        with open(self.filename, 'wb') as f:
            f.write(self.valid_body)
        with self.assertRaises(AssertionError):
            _assertBody(self.invalid_body, self.filename)

    def test_assert_body_empty(self):
        with open(self.filename, 'wb') as f:
            f.write(self.empty_body)
        _assertBody(self.empty_body, self.filename)

    def test_assert_body_with_newlines(self):
        body_with_newlines = b'This is a test body.\n'
        with open(self.filename, 'wb') as f:
            f.write(body_with_newlines)
        _assertBody(body_with_newlines.replace(b'\n', b''), self.filename)

    def test_assert_body_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            _assertBody(self.valid_body, 'non_existent_file.py')

    def tearDown(self):
        cleanUp()