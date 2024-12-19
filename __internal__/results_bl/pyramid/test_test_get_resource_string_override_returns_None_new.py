import os
import unittest
from pyramid.testing import cleanUp
from pyramid.exceptions import ConfigurationError
from io import BytesIO
from tests.test_config import pkgs

class TestAssertBody(unittest.TestCase):

    def setUp(self):
        self.filename = 'test_assets.py'
        self.valid_body = b'This is a test body without new lines or carriage returns.'
        self.invalid_body = b'This is an invalid body.'
        self.empty_body = b''

    def test_assert_body_valid(self):
        with open(os.path.join(os.path.dirname(__file__), self.filename), 'wb') as f:
            f.write(self.valid_body)
        _assertBody(self.valid_body, os.path.join(os.path.dirname(__file__), self.filename))

    def test_assert_body_invalid(self):
        with self.assertRaises(AssertionError):
            _assertBody(self.invalid_body, os.path.join(os.path.dirname(__file__), self.filename))

    def test_assert_body_empty(self):
        with open(os.path.join(os.path.dirname(__file__), self.filename), 'wb') as f:
            f.write(self.empty_body)
        with self.assertRaises(AssertionError):
            _assertBody(self.valid_body, os.path.join(os.path.dirname(__file__), self.filename))

    def test_assert_body_with_carriage_return(self):
        body_with_cr = b'This is a test body with a carriage return.\r'
        with open(os.path.join(os.path.dirname(__file__), self.filename), 'wb') as f:
            f.write(body_with_cr)
        _assertBody(body_with_cr.replace(b'\r', b''), os.path.join(os.path.dirname(__file__), self.filename))

    def test_assert_body_with_new_line(self):
        body_with_nl = b'This is a test body with a new line.\n'
        with open(os.path.join(os.path.dirname(__file__), self.filename), 'wb') as f:
            f.write(body_with_nl)
        _assertBody(body_with_nl.replace(b'\n', b''), os.path.join(os.path.dirname(__file__), self.filename))

    def tearDown(self):
        cleanUp()