import os
import unittest
from pyramid.testing import DummyRequest

class TestAssertBody(unittest.TestCase):
    
    def setUp(self):
        self.here = os.path.dirname(__file__)
        self.fn_valid = os.path.join(self.here, 'fixtures/static/index.html')
        self.fn_invalid = os.path.join(self.here, 'fixtures/static/invalid.html')
        self.body_valid = b'Valid content without newlines or carriage returns'
        self.body_invalid = b'Invalid content'

    def test_assert_body_valid(self):
        with open(self.fn_valid, 'wb') as f:
            f.write(self.body_valid)
        _assertBody(self.body_valid, self.fn_valid)

    def test_assert_body_invalid(self):
        with open(self.fn_valid, 'wb') as f:
            f.write(self.body_valid)
        with self.assertRaises(AssertionError):
            _assertBody(self.body_invalid, self.fn_valid)

    def test_assert_body_with_newlines(self):
        body_with_newlines = b'Line 1\nLine 2\r\n'
        with open(self.fn_valid, 'wb') as f:
            f.write(body_with_newlines.replace(b'\n', b'').replace(b'\r', b''))
        _assertBody(body_with_newlines, self.fn_valid)

    def test_assert_body_empty(self):
        empty_body = b''
        with open(self.fn_valid, 'wb') as f:
            f.write(empty_body)
        _assertBody(empty_body, self.fn_valid)

    def test_assert_body_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            _assertBody(self.body_valid, self.fn_invalid)

if __name__ == '__main__':
    unittest.main()