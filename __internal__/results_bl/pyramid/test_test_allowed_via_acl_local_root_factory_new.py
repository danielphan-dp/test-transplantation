import os
import unittest
from pyramid.testing import DummyRequest

class TestAssertBody(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__), 'fixtures/static/index.html')
        self.valid_body = b'Valid body content'
        with open(self.filename, 'wb') as f:
            f.write(self.valid_body)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_assert_body_equal(self):
        _assertBody(self.valid_body, self.filename)

    def test_assert_body_not_equal(self):
        with self.assertRaises(AssertionError):
            _assertBody(b'Invalid body content', self.filename)

    def test_assert_body_with_newlines(self):
        body_with_newlines = b'Valid body content\n'
        _assertBody(body_with_newlines, self.filename)

    def test_assert_body_with_carriage_returns(self):
        body_with_carriage_returns = b'Valid body content\r'
        _assertBody(body_with_carriage_returns, self.filename)

    def test_assert_body_empty(self):
        empty_body = b''
        with open(self.filename, 'wb') as f:
            f.write(empty_body)
        with self.assertRaises(AssertionError):
            _assertBody(self.valid_body, self.filename)

    def test_assert_body_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            _assertBody(self.valid_body, 'non_existent_file.html')