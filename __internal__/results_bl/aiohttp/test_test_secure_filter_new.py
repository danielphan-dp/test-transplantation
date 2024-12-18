import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.jar.update_cookies({'shared-cookie': 'value1', 'secure-cookie': 'value2'}, URL("http://secure.com/"))
        self.cookies_to_send = self.jar.filter_cookies(URL("http://secure.com/"))
        self.cookies_to_receive = {'shared-cookie': 'value1', 'secure-cookie': 'value2'}

    def test_request_reply_with_same_url_http(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://secure.com/")
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie"})
        self.assertEqual(set(cookies_received.keys()), {"shared-cookie"})

    def test_request_reply_with_same_url_https(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("https://secure.com/")
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie", "secure-cookie"})
        self.assertEqual(set(cookies_received.keys()), {"shared-cookie", "secure-cookie"})

    def test_request_reply_with_different_url(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://different.com/")
        self.assertEqual(set(cookies_sent.keys()), set())
        self.assertEqual(set(cookies_received.keys()), set())

    def test_request_reply_with_no_cookies(self):
        self.jar.clear()
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://secure.com/")
        self.assertEqual(set(cookies_sent.keys()), set())
        self.assertEqual(set(cookies_received.keys()), set())

    def test_request_reply_with_invalid_url(self):
        with self.assertRaises(ValueError):
            self.request_reply_with_same_url("invalid-url")

if __name__ == '__main__':
    unittest.main()