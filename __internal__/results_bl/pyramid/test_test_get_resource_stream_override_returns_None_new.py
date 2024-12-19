import os
import unittest
from pyramid.testing import cleanUp
from pyramid.exceptions import ConfigurationError
from io import BytesIO
from your_module import _assertBody  # Replace with the actual module name

class TestAssertBody(unittest.TestCase):

    def setUp(self):
        self.filename = 'test_assets.py'
        self.valid_body = b'This is a test body without new lines or carriage returns.'
        self.invalid_body = b'This is an invalid body.'

    def test_assert_body_valid(self):
        with open(self.filename, 'wb') as f:
            f.write(self.valid_body)
        _assertBody(self.valid_body, self.filename)

    def test_assert_body_invalid(self):
        with open(self.filename, 'wb') as f:
            f.write(self.valid_body)
        with self.assertRaises(AssertionError):
            _assertBody(self.invalid_body, self.filename)

    def test_assert_body_with_carriage_returns(self):
        body_with_cr = b'This is a test body with\r\nnew lines and\r carriage returns.'
        with open(self.filename, 'wb') as f:
            f.write(body_with_cr)
        _assertBody(body_with_cr.replace(b'\r', b'').replace(b'\n', b''), self.filename)

    def test_assert_body_empty_file(self):
        with open(self.filename, 'wb') as f:
            f.write(b'')
        with self.assertRaises(AssertionError):
            _assertBody(self.valid_body, self.filename)

    def test_assert_body_non_existent_file(self):
        with self.assertRaises(FileNotFoundError):
            _assertBody(self.valid_body, 'non_existent_file.py')

    def tearDown(self):
        cleanUp()

if __name__ == '__main__':
    unittest.main()