import os
import unittest
from pyramid.testing import cleanUp
from pyramid.exceptions import ConfigurationError

class TestAssertBody(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__), 'test_assets.py')
        self.valid_body = b'This is a test file content without new lines or carriage returns.'
        with open(self.filename, 'wb') as f:
            f.write(self.valid_body.replace(b'\n', b'').replace(b'\r', b''))

    def tearDown(self):
        cleanUp()

    def test_assert_body_valid(self):
        _assertBody(self.valid_body, self.filename)

    def test_assert_body_empty(self):
        with self.assertRaises(AssertionError):
            _assertBody(b'', self.filename)

    def test_assert_body_mismatched(self):
        with self.assertRaises(AssertionError):
            _assertBody(b'Invalid content', self.filename)

    def test_assert_body_with_carriage_return(self):
        body_with_cr = self.valid_body + b'\r'
        with self.assertRaises(AssertionError):
            _assertBody(body_with_cr, self.filename)

    def test_assert_body_with_new_line(self):
        body_with_nl = self.valid_body + b'\n'
        with self.assertRaises(AssertionError):
            _assertBody(body_with_nl, self.filename)

    def test_assert_body_non_existent_file(self):
        with self.assertRaises(FileNotFoundError):
            _assertBody(self.valid_body, 'non_existent_file.py')