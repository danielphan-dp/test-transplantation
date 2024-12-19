import os
import unittest
from pyramid.testing import DummyRequest

class TestAssertBody(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join('fixtures/static/.hiddenfile')
        self.valid_body = b'valid content'
        self.invalid_body = b'invalid content'
        with open(self.filename, 'wb') as f:
            f.write(self.valid_body)

    def test_assert_body_valid(self):
        _assertBody(self.valid_body, self.filename)

    def test_assert_body_invalid(self):
        with self.assertRaises(AssertionError):
            _assertBody(self.invalid_body, self.filename)

    def test_assert_body_empty(self):
        empty_body = b''
        with open(self.filename, 'wb') as f:
            f.write(empty_body)
        _assertBody(empty_body, self.filename)

    def test_assert_body_with_newlines(self):
        body_with_newlines = b'valid content\n'
        with open(self.filename, 'wb') as f:
            f.write(self.valid_body)
        _assertBody(body_with_newlines, self.filename)

    def test_assert_body_with_carriage_returns(self):
        body_with_carriage_returns = b'valid content\r'
        with open(self.filename, 'wb') as f:
            f.write(self.valid_body)
        _assertBody(body_with_carriage_returns, self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

if __name__ == '__main__':
    unittest.main()