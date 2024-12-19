import unittest
from pyramid.util import text_

class TestCookieValue(unittest.TestCase):

    def setUp(self):
        self.ticket = self._makeOne('secret', 'userid', '198.51.100.1', time=10, hashalg='sha256')

    def test_empty_tokens(self):
        self.ticket.kw = {}
        result = self.ticket.cookie_value()
        self.assertEqual(result, 'b3e7156db4f8abde4439c4a6499a0668f9e7ffd7fa27b798400ecdade8d76c530000000auserid!')

    def test_single_token(self):
        self.ticket.kw = {'tokens': ['token1']}
        result = self.ticket.cookie_value()
        self.assertEqual(result, 'b3e7156db4f8abde4439c4a6499a0668f9e7ffd7fa27b798400ecdade8d76c530000000auserid!')

    def test_multiple_tokens(self):
        self.ticket.kw = {'tokens': ['token1', 'token2']}
        result = self.ticket.cookie_value()
        self.assertEqual(result, 'b3e7156db4f8abde4439c4a6499a0668f9e7ffd7fa27b798400ecdade8d76c530000000auserid!')

    def test_bytes_in_kw(self):
        self.ticket.kw = {'key': b'byte_value'}
        result = self.ticket.cookie_value()
        self.assertIn('key=byte_value', result)

    def test_no_secret(self):
        self.ticket.secret = None
        result = self.ticket.cookie_value()
        self.assertIn('userid=', result)

    def test_no_userid(self):
        self.ticket.userid = None
        result = self.ticket.cookie_value()
        self.assertIn('secret=', result)

    def test_no_remote_addr(self):
        self.ticket.remote_addr = None
        result = self.ticket.cookie_value()
        self.assertIn('userid=', result)

    def test_tokens_as_none(self):
        self.ticket.kw = {'tokens': None}
        result = self.ticket.cookie_value()
        self.assertNotIn('tokens=', result)