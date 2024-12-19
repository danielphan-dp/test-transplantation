import unittest
from pyramid.testing import DummyRequest

class TestCookieValue(unittest.TestCase):

    def setUp(self):
        self.ticket = self._makeOne('secret', 'userid', '192.168.1.1')

    def _makeOne(self, secret, userid, remote_addr, **kwargs):
        ticket = DummyRequest()
        ticket.secret = secret
        ticket.userid = userid
        ticket.remote_addr = remote_addr
        ticket.kw = kwargs
        return ticket

    def test_no_tokens(self):
        result = self.ticket.cookie_value()
        self.assertEqual(result, 'remote_addr=192.168.1.1/secret=secret/userid=userid')

    def test_with_tokens(self):
        self.ticket.kw['tokens'] = ['token1', 'token2']
        result = self.ticket.cookie_value()
        self.assertEqual(result, 'remote_addr=192.168.1.1/secret=secret/userid=userid/tokens=token1|token2')

    def test_bytes_value(self):
        self.ticket.secret = b'secret_bytes'
        result = self.ticket.cookie_value()
        self.assertEqual(result, 'remote_addr=192.168.1.1/secret=secret_bytes/userid=userid')

    def test_empty_userid(self):
        self.ticket.userid = ''
        result = self.ticket.cookie_value()
        self.assertEqual(result, 'remote_addr=192.168.1.1/secret=secret/userid=')

    def test_multiple_kw_arguments(self):
        self.ticket.kw = {'key1': 'value1', 'key2': 'value2'}
        result = self.ticket.cookie_value()
        self.assertEqual(result, 'key1=value1/key2=value2/remote_addr=192.168.1.1/secret=secret/userid=userid')