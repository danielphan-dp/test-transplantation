import unittest
from pyramid.testing import DummyRequest

class TestCookieValue(unittest.TestCase):

    def setUp(self):
        self.ticket = self._makeOne('secret', 'userid', '0.0.0.0')

    def _makeOne(self, secret, userid, remote_addr, **kwargs):
        class Ticket:
            def __init__(self, secret, userid, remote_addr, **kwargs):
                self.secret = secret
                self.userid = userid
                self.remote_addr = remote_addr
                self.kw = kwargs

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

        return Ticket(secret, userid, remote_addr, **kwargs)

    def test_cookie_value_no_tokens(self):
        result = self.ticket.cookie_value()
        self.assertEqual(result, '66f9cc3e423dc57c91df696cf3d1f0d80000000userid!0.0.0.0!')

    def test_cookie_value_empty_tokens(self):
        ticket = self._makeOne('secret', 'userid', '0.0.0.0', tokens=())
        result = ticket.cookie_value()
        self.assertEqual(result, '66f9cc3e423dc57c91df696cf3d1f0d80000000userid!0.0.0.0!')

    def test_cookie_value_single_token(self):
        ticket = self._makeOne('secret', 'userid', '0.0.0.0', tokens=('a',))
        result = ticket.cookie_value()
        self.assertEqual(result, '66f9cc3e423dc57c91df696cf3d1f0d80000000userid!0.0.0.0!a!')

    def test_cookie_value_bytes_in_fields(self):
        ticket = self._makeOne(b'secret', b'userid', b'0.0.0.0', tokens=('a', 'b'))
        result = ticket.cookie_value()
        self.assertEqual(result, '66f9cc3e423dc57c91df696cf3d1f0d80000000userid!0.0.0.0!a|b!')

    def test_cookie_value_with_additional_kwargs(self):
        ticket = self._makeOne('secret', 'userid', '0.0.0.0', tokens=('a', 'b'), extra='value')
        result = ticket.cookie_value()
        self.assertEqual(result, '66f9cc3e423dc57c91df696cf3d1f0d80000000userid!0.0.0.0!a|b!extra=value!')