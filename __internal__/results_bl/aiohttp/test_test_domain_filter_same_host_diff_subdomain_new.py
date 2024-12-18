import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.jar.update_cookies({'shared-cookie': 'value1', 'domain-cookie': 'value2', 'dotted-domain-cookie': 'value3'})
        self.cookies_to_receive = {'unconstrained-cookie': 'value4', 'domain-cookie': 'value5', 'dotted-domain-cookie': 'value6'}

    def test_request_reply_with_same_url_empty_cookies(self):
        cookies_sent, cookies_received = self.jar.request_reply_with_same_url("http://example.com/")
        self.assertEqual(set(cookies_sent.keys()), set())
        self.assertEqual(set(cookies_received.keys()), set())

    def test_request_reply_with_same_url_no_matching_domain(self):
        self.jar.update_cookies({'non-matching-cookie': 'value7'})
        cookies_sent, cookies_received = self.jar.request_reply_with_same_url("http://unrelated.com/")
        self.assertEqual(set(cookies_sent.keys()), {'non-matching-cookie'})
        self.assertEqual(set(cookies_received.keys()), set())

    def test_request_reply_with_same_url_multiple_cookies(self):
        self.jar.update_cookies({'cookie1': 'value1', 'cookie2': 'value2'})
        self.cookies_to_receive = {'cookie2': 'new_value2', 'cookie3': 'value3'}
        cookies_sent, cookies_received = self.jar.request_reply_with_same_url("http://example.com/")
        self.assertEqual(set(cookies_sent.keys()), {'cookie1', 'cookie2'})
        self.assertEqual(set(cookies_received.keys()), {'cookie2', 'cookie3'})

    def test_request_reply_with_same_url_different_subdomain(self):
        self.jar.update_cookies({'shared-cookie': 'value1', 'domain-cookie': 'value2'})
        self.cookies_to_receive = {'unconstrained-cookie': 'value4', 'domain-cookie': 'value5'}
        cookies_sent, cookies_received = self.jar.request_reply_with_same_url("http://sub.example.com/")
        self.assertEqual(set(cookies_sent.keys()), {'shared-cookie', 'domain-cookie'})
        self.assertEqual(set(cookies_received.keys()), {'unconstrained-cookie', 'domain-cookie'})

if __name__ == '__main__':
    unittest.main()