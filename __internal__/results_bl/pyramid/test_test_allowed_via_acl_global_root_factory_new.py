import os
import unittest
from pyramid.testing import DummyRequest

class TestAssertBody(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__), 'fixtures/static/index.html')
        self.valid_body = b'Valid content without newlines or carriage returns'
        with open(self.filename, 'wb') as f:
            f.write(self.valid_body)

    def test_assert_body_success(self):
        _assertBody(self.valid_body, self.filename)

    def test_assert_body_failure(self):
        with self.assertRaises(AssertionError):
            _assertBody(b'Invalid content', self.filename)

    def test_assert_body_with_newlines(self):
        body_with_newlines = b'Valid content\nwith newlines\r\n'
        _assertBody(body_with_newlines, self.filename)

    def test_assert_body_with_carriage_returns(self):
        body_with_carriage_returns = b'Valid content\rwith carriage returns\n'
        _assertBody(body_with_carriage_returns, self.filename)

    def test_assert_body_empty(self):
        empty_body = b''
        with open(self.filename, 'wb') as f:
            f.write(empty_body)
        _assertBody(empty_body, self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

if __name__ == '__main__':
    unittest.main()