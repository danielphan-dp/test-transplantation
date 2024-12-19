import os
import unittest
from pyramid.testing import DummyRequest

class TestAssertBody(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join('fixtures/static/index.html')
        self.valid_body = b'Valid content without newlines or carriage returns'
        self.invalid_body = b'Invalid content'
        with open(self.filename, 'wb') as f:
            f.write(self.valid_body)

    def test_assert_body_valid(self):
        _assertBody(self.valid_body, self.filename)

    def test_assert_body_invalid(self):
        with self.assertRaises(AssertionError):
            _assertBody(self.invalid_body, self.filename)

    def test_assert_body_with_carriage_return(self):
        body_with_cr = b'Valid content without newlines or carriage returns\r'
        with self.assertRaises(AssertionError):
            _assertBody(body_with_cr, self.filename)

    def test_assert_body_with_newline(self):
        body_with_nl = b'Valid content without newlines or carriage returns\n'
        with self.assertRaises(AssertionError):
            _assertBody(body_with_nl, self.filename)

    def test_assert_body_empty(self):
        empty_body = b''
        with self.assertRaises(AssertionError):
            _assertBody(empty_body, self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

if __name__ == '__main__':
    unittest.main()