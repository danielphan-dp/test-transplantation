import os
import unittest
from pyramid.testing import cleanUp
from pyramid.exceptions import ConfigurationError

class TestAssertBody(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__), 'test_assets.py')
        self.valid_body = b'This is a test content.'
        with open(self.filename, 'wb') as f:
            f.write(self.valid_body)

    def tearDown(self):
        cleanUp()

    def test_assert_body_valid(self):
        _assertBody(self.valid_body, self.filename)

    def test_assert_body_empty(self):
        with self.assertRaises(AssertionError):
            _assertBody(b'', self.filename)

    def test_assert_body_mismatched(self):
        with open(self.filename, 'wb') as f:
            f.write(b'Another content.')
        with self.assertRaises(AssertionError):
            _assertBody(self.valid_body, self.filename)

    def test_assert_body_with_newlines(self):
        body_with_newlines = b'This is a test content.\n'
        _assertBody(body_with_newlines, self.filename)

    def test_assert_body_with_carriage_returns(self):
        body_with_carriage_returns = b'This is a test content.\r'
        _assertBody(body_with_carriage_returns, self.filename)

    def test_assert_body_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            _assertBody(self.valid_body, 'nonexistent_file.py')