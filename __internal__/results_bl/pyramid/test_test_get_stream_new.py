import os
import unittest
from pyramid.testing import cleanUp
from pyramid.exceptions import ConfigurationError
from io import BytesIO

class TestAssertBody(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__), 'test_assets.py')
        self.valid_body = b'print("Hello World")'
        with open(self.filename, 'wb') as f:
            f.write(self.valid_body)

    def tearDown(self):
        cleanUp()

    def test_assert_body_valid(self):
        with open(self.filename, 'rb') as f:
            body = f.read()
            _assertBody(body, self.filename)

    def test_assert_body_empty(self):
        empty_body = b''
        with open(self.filename, 'wb') as f:
            f.write(empty_body)
        with self.assertRaises(AssertionError):
            _assertBody(self.valid_body, self.filename)

    def test_assert_body_mismatched(self):
        mismatched_body = b'print("Goodbye World")'
        with open(self.filename, 'wb') as f:
            f.write(self.valid_body)
        with self.assertRaises(AssertionError):
            _assertBody(mismatched_body, self.filename)

    def test_assert_body_with_newlines(self):
        body_with_newlines = b'print("Hello World")\n'
        with open(self.filename, 'wb') as f:
            f.write(self.valid_body)
        _assertBody(body_with_newlines, self.filename)

    def test_assert_body_with_carriage_returns(self):
        body_with_carriage_returns = b'print("Hello World")\r'
        with open(self.filename, 'wb') as f:
            f.write(self.valid_body)
        _assertBody(body_with_carriage_returns, self.filename)

    def test_assert_body_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            _assertBody(self.valid_body, 'invalid_file.py')