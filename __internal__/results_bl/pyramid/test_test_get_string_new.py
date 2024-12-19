import os
import unittest
from pyramid.testing import cleanUp
from pyramid.exceptions import ConfigurationError

class TestAssertBody(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__), 'test_assets.py')

    def test_assert_body_equal(self):
        body = b'This is a test content without new lines or carriage returns.'
        with open(self.filename, 'wb') as f:
            f.write(body.replace(b'\n', b'').replace(b'\r', b''))
        _assertBody(body, self.filename)

    def test_assert_body_with_carriage_return(self):
        body = b'This is a test content with a carriage return.\r'
        with open(self.filename, 'wb') as f:
            f.write(body.replace(b'\n', b'').replace(b'\r', b''))
        _assertBody(body, self.filename)

    def test_assert_body_with_new_line(self):
        body = b'This is a test content with a new line.\n'
        with open(self.filename, 'wb') as f:
            f.write(body.replace(b'\r', b'').replace(b'\n', b''))
        _assertBody(body, self.filename)

    def test_assert_body_not_equal(self):
        body = b'This is a different content.'
        with open(self.filename, 'wb') as f:
            f.write(b'This is a test content without new lines or carriage returns.')
        with self.assertRaises(AssertionError):
            _assertBody(body, self.filename)

    def test_assert_body_empty(self):
        body = b''
        with open(self.filename, 'wb') as f:
            f.write(b'')
        _assertBody(body, self.filename)

    def tearDown(self):
        cleanUp()