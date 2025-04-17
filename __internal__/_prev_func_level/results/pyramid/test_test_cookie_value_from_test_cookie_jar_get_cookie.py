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

    def test_cookie_value_with_no_tokens(self):
        ticket = self._makeOne('secret', 'userid', '0.0.0.0')
        result = ticket.cookie_value()
        self.assertEqual(result, 'secret=secret/remote_addr=0.0.0.0/userid=userid')

    def test_cookie_value_with_empty_tokens(self):
        ticket = self._makeOne('secret', 'userid', '0.0.0.0', tokens=())
        result = ticket.cookie_value()
        self.assertEqual(result, 'secret=secret/remote_addr=0.0.0.0/userid=userid')

    def test_cookie_value_with_single_token(self):
        ticket = self._makeOne('secret', 'userid', '0.0.0.0', tokens=('token1',))
        result = ticket.cookie_value()
        self.assertEqual(result, 'secret=secret/remote_addr=0.0.0.0/tokens=token1/userid=userid')

    def test_cookie_value_with_multiple_tokens(self):
        ticket = self._makeOne('secret', 'userid', '0.0.0.0', tokens=('token1', 'token2'))
        result = ticket.cookie_value()
        self.assertEqual(result, 'secret=secret/remote_addr=0.0.0.0/tokens=token1|token2/userid=userid')

    def test_cookie_value_with_bytes(self):
        ticket = self._makeOne(b'secret', b'userid', b'0.0.0.0', tokens=(b'token1', b'token2'))
        result = ticket.cookie_value()
        self.assertEqual(result, 'secret=secret/remote_addr=0.0.0.0/tokens=token1|token2/userid=userid')

    def test_cookie_value_with_special_characters(self):
        ticket = self._makeOne('secre$t', 'user@id', '0.0.0.0', tokens=('token#1', 'token&2'))
        result = ticket.cookie_value()
        self.assertEqual(result, 'secret=secre$t/remote_addr=0.0.0.0/tokens=token#1|token&2/userid=user@id')

if __name__ == '__main__':
    unittest.main()