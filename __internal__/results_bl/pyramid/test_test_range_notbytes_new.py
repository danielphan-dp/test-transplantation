import os
import unittest
from pyramid.testing import DummyRequest

class TestAssertBody(unittest.TestCase):
    
    def setUp(self):
        self.filename = os.path.join('fixtures/static/index.html')
        self.valid_body = b'Valid content without newlines or carriage returns'
        self.invalid_body = b'Invalid content'
        with open(self.filename, 'wb') as f:
            f.write(self.valid_body.replace(b'\n', b'').replace(b'\r', b''))

    def test_assert_body_valid(self):
        _assertBody(self.valid_body, self.filename)

    def test_assert_body_invalid(self):
        with self.assertRaises(AssertionError):
            _assertBody(self.invalid_body, self.filename)

    def test_assert_body_with_newlines(self):
        body_with_newlines = b'Valid content\nwith newlines\r\n'
        _assertBody(body_with_newlines.replace(b'\n', b'').replace(b'\r', b''), self.filename)

    def test_assert_body_empty(self):
        empty_body = b''
        with self.assertRaises(AssertionError):
            _assertBody(empty_body, self.filename)

    def test_assert_body_nonexistent_file(self):
        nonexistent_file = os.path.join('fixtures/static/nonexistent.html')
        with self.assertRaises(FileNotFoundError):
            _assertBody(self.valid_body, nonexistent_file)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

if __name__ == '__main__':
    unittest.main()