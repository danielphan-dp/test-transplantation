import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie()
        self.cookies_to_receive = SimpleCookie()

    def test_empty_cookies(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/")
        self.assertEqual(cookies_sent, SimpleCookie())
        self.assertEqual(cookies_received, SimpleCookie())

    def test_no_matching_domain(self):
        self.cookies_to_send['test-cookie'] = 'value'
        self.cookies_to_receive['unrelated-cookie'] = 'value'
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/")
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})
        self.assertEqual(set(cookies_received.keys()), set())

    def test_multiple_cookies(self):
        self.cookies_to_send['cookie1'] = 'value1'
        self.cookies_to_send['cookie2'] = 'value2'
        self.cookies_to_receive['cookie3'] = 'value3'
        self.cookies_to_receive['cookie4'] = 'value4'
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/")
        self.assertEqual(set(cookies_sent.keys()), {"cookie1", "cookie2"})
        self.assertEqual(set(cookies_received.keys()), {"cookie3", "cookie4"})

    def test_cookie_with_path(self):
        self.cookies_to_send['path-cookie'] = 'value'
        self.cookies_to_receive['path-received-cookie'] = 'value'
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/path")
        self.assertEqual(set(cookies_sent.keys()), {"path-cookie"})
        self.assertEqual(set(cookies_received.keys()), {"path-received-cookie"})

    def test_cookie_with_expiration(self):
        self.cookies_to_send['expiring-cookie'] = 'value'
        self.cookies_to_send['expiring-cookie']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/")
        self.assertEqual(set(cookies_sent.keys()), {"expiring-cookie"})
        self.assertEqual(set(cookies_received.keys()), set())

    def request_reply_with_same_url(self, url: str) -> Tuple['BaseCookie[str]', SimpleCookie]:
        self.jar.update_cookies(self.cookies_to_send)
        cookies_sent = self.jar.filter_cookies(URL(url))
        self.jar.clear()
        self.jar.update_cookies(self.cookies_to_receive, URL(url))
        cookies_received = SimpleCookie()
        for cookie in self.jar:
            dict.__setitem__(cookies_received, cookie.key, cookie)
        self.jar.clear()
        return (cookies_sent, cookies_received)