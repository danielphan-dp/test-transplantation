import os
import unittest
from pyramid.testing import DummyRequest

class TestAssertBody(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__), 'fixtures/minimal.txt')

    def test_assert_body_equal(self):
        body = b'This is a test content.'
        with open(self.filename, 'wb') as f:
            f.write(body)
        _assertBody(body, self.filename)

    def test_assert_body_not_equal(self):
        body = b'This is a different content.'
        with open(self.filename, 'wb') as f:
            f.write(b'This is a test content.')
        with self.assertRaises(AssertionError):
            _assertBody(body, self.filename)

    def test_assert_body_with_newlines(self):
        body = b'This is a test content.\n'
        with open(self.filename, 'wb') as f:
            f.write(b'This is a test content.')
        _assertBody(body, self.filename)

    def test_assert_body_with_carriage_returns(self):
        body = b'This is a test content.\r'
        with open(self.filename, 'wb') as f:
            f.write(b'This is a test content.')
        _assertBody(body, self.filename)

    def test_assert_body_empty(self):
        body = b''
        with open(self.filename, 'wb') as f:
            f.write(b'')
        _assertBody(body, self.filename)

    def test_assert_body_file_not_found(self):
        body = b'This is a test content.'
        with self.assertRaises(FileNotFoundError):
            _assertBody(body, 'non_existent_file.txt')