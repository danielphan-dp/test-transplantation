import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie()
        self.cookies_to_receive = SimpleCookie()

    def request_reply_with_same_url(self, url: str):
        self.jar.update_cookies(self.cookies_to_send)
        cookies_sent = self.jar.filter_cookies(URL(url))
        self.jar.clear()
        self.jar.update_cookies(self.cookies_to_receive, URL(url))
        cookies_received = SimpleCookie()
        for cookie in self.jar:
            dict.__setitem__(cookies_received, cookie.key, cookie)
        self.jar.clear()
        return (cookies_sent, cookies_received)

    def test_empty_cookies(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://emptycookies.com")
        self.assertEqual(len(cookies_sent), 0)
        self.assertEqual(len(cookies_received), 0)

    def test_single_cookie_sent(self):
        self.cookies_to_send['test-cookie'] = 'value'
        cookies_sent, _ = self.request_reply_with_same_url("http://singlecookie.com")
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})

    def test_single_cookie_received(self):
        self.cookies_to_receive['received-cookie'] = 'value'
        _, cookies_received = self.request_reply_with_same_url("http://singlecookie.com")
        self.assertEqual(set(cookies_received.keys()), {"received-cookie"})

    def test_path_filtering(self):
        self.cookies_to_send['shared-cookie'] = 'value'
        self.cookies_to_send['no-path-cookie'] = 'value'
        self.cookies_to_send['path1-cookie'] = 'value'
        self.cookies_to_send['path2-cookie'] = 'value'
        self.cookies_to_send['path3-cookie'] = 'value'
        cookies_sent, _ = self.request_reply_with_same_url("http://pathtest.com/one/two")
        self.assertEqual(
            set(cookies_sent.keys()),
            {
                "shared-cookie",
                "no-path-cookie",
                "path1-cookie",
                "path2-cookie",
                "path3-cookie",
            },
        )

    def test_no_cookies_sent_or_received(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://nocookies.com")
        self.assertEqual(len(cookies_sent), 0)
        self.assertEqual(len(cookies_received), 0)

    def test_multiple_cookies_received(self):
        self.cookies_to_receive['cookie1'] = 'value1'
        self.cookies_to_receive['cookie2'] = 'value2'
        _, cookies_received = self.request_reply_with_same_url("http://multiplecookies.com")
        self.assertEqual(set(cookies_received.keys()), {"cookie1", "cookie2"})