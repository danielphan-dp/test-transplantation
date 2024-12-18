import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.jar.update_cookies({'shared-cookie': 'value1', 'different-domain-cookie': 'value2'})
        self.cookies_to_receive = {'unconstrained-cookie': 'value3', 'different-domain-cookie': 'value4'}

    def test_request_reply_with_same_url_empty_cookies(self):
        cookies_sent, cookies_received = self.jar.request_reply_with_same_url("http://empty.org/")
        self.assertEqual(set(cookies_sent.keys()), set())
        self.assertEqual(set(cookies_received.keys()), set())

    def test_request_reply_with_same_url_no_sent_cookies(self):
        self.jar.clear()
        cookies_sent, cookies_received = self.jar.request_reply_with_same_url("http://no-sent.org/")
        self.assertEqual(set(cookies_sent.keys()), set())
        self.assertEqual(set(cookies_received.keys()), {"unconstrained-cookie", "different-domain-cookie"})

    def test_request_reply_with_same_url_same_domain(self):
        cookies_sent, cookies_received = self.jar.request_reply_with_same_url("http://same.org/")
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie", "different-domain-cookie"})
        self.assertEqual(set(cookies_received.keys()), {"unconstrained-cookie", "different-domain-cookie"})

    def test_request_reply_with_same_url_invalid_url(self):
        with self.assertRaises(ValueError):
            self.jar.request_reply_with_same_url("invalid-url")

    def test_request_reply_with_same_url_multiple_cookies(self):
        self.jar.update_cookies({'cookie1': 'value1', 'cookie2': 'value2'})
        cookies_sent, cookies_received = self.jar.request_reply_with_same_url("http://multiple.org/")
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie", "different-domain-cookie", "cookie1", "cookie2"})
        self.assertEqual(set(cookies_received.keys()), {"unconstrained-cookie", "different-domain-cookie"})