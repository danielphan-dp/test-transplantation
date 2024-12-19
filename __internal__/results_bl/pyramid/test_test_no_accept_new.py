import os
import unittest
from pyramid.testing import DummyRequest

class TestAssertBody(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__), 'fixtures/static/encoded.html')

    def test_assert_body_equal(self):
        body = b'This is a test body without new lines or carriage returns.'
        with open(self.filename, 'wb') as f:
            f.write(body)
        _assertBody(body, self.filename)

    def test_assert_body_not_equal(self):
        body = b'This is a different body.'
        with self.assertRaises(AssertionError):
            _assertBody(body, self.filename)

    def test_assert_body_with_carriage_returns(self):
        body = b'This is a test body with\r\nnew lines and\r carriage returns.'
        with open(self.filename, 'wb') as f:
            f.write(body.replace(b'\r', b'').replace(b'\n', b''))
        _assertBody(body.replace(b'\r', b'').replace(b'\n', b''), self.filename)

    def test_assert_body_empty(self):
        body = b''
        with open(self.filename, 'wb') as f:
            f.write(b'')
        _assertBody(body, self.filename)

    def test_assert_body_file_not_found(self):
        body = b'Test body'
        with self.assertRaises(FileNotFoundError):
            _assertBody(body, 'non_existent_file.html')