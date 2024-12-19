import os
import unittest
from pyramid.testing import DummyRequest

class TestAssertBody(unittest.TestCase):

    def setUp(self):
        self.here = os.path.dirname(__file__)
        self.fn_valid = os.path.join(self.here, 'fixtures/static/index.html')
        self.fn_invalid = os.path.join(self.here, 'fixtures/static/invalid.html')
        self.body_valid = b'<html><body>Test</body></html>'
        self.body_invalid = b'<html><body>Invalid</body></html>'
        with open(self.fn_valid, 'wb') as f:
            f.write(self.body_valid)

    def test_assert_body_valid(self):
        res = DummyRequest()
        res.body = self.body_valid
        _assertBody(res.body, self.fn_valid)

    def test_assert_body_invalid(self):
        res = DummyRequest()
        res.body = self.body_invalid
        with self.assertRaises(AssertionError):
            _assertBody(res.body, self.fn_valid)

    def test_assert_body_empty(self):
        res = DummyRequest()
        res.body = b''
        with self.assertRaises(AssertionError):
            _assertBody(res.body, self.fn_valid)

    def test_assert_body_with_newlines(self):
        res = DummyRequest()
        res.body = b'<html>\n<body>\r\nTest\r\n</body>\n</html>'
        _assertBody(res.body, self.fn_valid)

    def test_assert_body_file_not_found(self):
        res = DummyRequest()
        res.body = self.body_valid
        with self.assertRaises(FileNotFoundError):
            _assertBody(res.body, self.fn_invalid)

    def tearDown(self):
        if os.path.exists(self.fn_valid):
            os.remove(self.fn_valid)