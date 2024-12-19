import os
import unittest
from pyramid.testing import DummyRequest

class TestAssertBody(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__), 'fixtures/static/index.html')

    def test_assert_body_equal(self):
        body = b'This is a test body.'
        with open(self.filename, 'wb') as f:
            f.write(body)
        _assertBody(body, self.filename)

    def test_assert_body_with_newlines(self):
        body = b'This is a test body.\n'
        with open(self.filename, 'wb') as f:
            f.write(b'This is a test body.')
        _assertBody(body, self.filename)

    def test_assert_body_with_carriage_returns(self):
        body = b'This is a test body.\r'
        with open(self.filename, 'wb') as f:
            f.write(b'This is a test body.')
        _assertBody(body, self.filename)

    def test_assert_body_not_equal(self):
        body = b'This is a different body.'
        with open(self.filename, 'wb') as f:
            f.write(b'This is a test body.')
        with self.assertRaises(AssertionError):
            _assertBody(body, self.filename)

    def test_assert_body_empty_file(self):
        body = b'This is a test body.'
        with open(self.filename, 'wb') as f:
            f.write(b'')
        with self.assertRaises(AssertionError):
            _assertBody(body, self.filename)

    def test_assert_body_empty_body(self):
        body = b''
        with open(self.filename, 'wb') as f:
            f.write(b'This is a test body.')
        with self.assertRaises(AssertionError):
            _assertBody(body, self.filename)

    def test_assert_body_unicode_filename(self):
        body = b'This is a test body.'
        filename = self.filename.encode('utf-8')
        with open(self.filename, 'wb') as f:
            f.write(body)
        _assertBody(body, filename)

if __name__ == '__main__':
    unittest.main()