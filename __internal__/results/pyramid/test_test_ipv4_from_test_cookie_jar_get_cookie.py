import unittest
from pyramid import testing

class TestAuthTicket(unittest.TestCase):

    def _makeOne(self, secret, userid, remote_addr, **kw):
        class AuthTicket:
            def __init__(self, secret, userid, remote_addr, **kw):
                self.secret = secret
                self.userid = userid
                self.remote_addr = remote_addr
                self.kw = kw

            def cookie_value(self):
                result = {'secret': self.secret, 'userid': self.userid, 'remote_addr': self.remote_addr}
                result.update(self.kw)
                tokens = result.pop('tokens', None)
                if tokens is not None:
                    tokens = '|'.join(tokens)
                    result['tokens'] = tokens
                items = sorted(result.items())
                new_items = []
                for (k, v) in items:
                    if isinstance(v, bytes):
                        v = text_(v)
                    new_items.append((k, v))
                result = '/'.join([f'{k}={v}' for (k, v) in new_items])
                return result

        return AuthTicket(secret, userid, remote_addr, **kw)

    def test_empty_tokens(self):
        ticket = self._makeOne('secret', 'userid', '198.51.100.1')
        result = ticket.cookie_value()
        self.assertEqual(result, 'remote_addr=198.51.100.1/secret=secret/userid=userid')

    def test_single_token(self):
        ticket = self._makeOne('secret', 'userid', '198.51.100.1', tokens=['token1'])
        result = ticket.cookie_value()
        self.assertEqual(result, 'remote_addr=198.51.100.1/secret=secret/tokens=token1/userid=userid')

    def test_multiple_tokens(self):
        ticket = self._makeOne('secret', 'userid', '198.51.100.1', tokens=['token1', 'token2'])
        result = ticket.cookie_value()
        self.assertEqual(result, 'remote_addr=198.51.100.1/secret=secret/tokens=token1|token2/userid=userid')

    def test_bytes_in_values(self):
        ticket = self._makeOne(b'secret', b'userid', b'198.51.100.1', tokens=[b'token1'])
        result = ticket.cookie_value()
        self.assertEqual(result, 'remote_addr=198.51.100.1/secret=secret/userid=userid/tokens=token1')

    def test_ipv6_address(self):
        ticket = self._makeOne('secret', 'userid', '2001:db8::1')
        result = ticket.cookie_value()
        self.assertEqual(result, 'remote_addr=2001:db8::1/secret=secret/userid=userid')

    def test_no_remote_addr(self):
        ticket = self._makeOne('secret', 'userid', None)
        result = ticket.cookie_value()
        self.assertEqual(result, 'remote_addr=None/secret=secret/userid=userid')

if __name__ == '__main__':
    unittest.main()