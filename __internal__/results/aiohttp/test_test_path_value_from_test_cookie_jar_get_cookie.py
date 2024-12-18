import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.cookies_to_send = SimpleCookie("test-cookie=val; Path=/;")
        self.cookies_to_receive = SimpleCookie(
            "unconstrained-cookie=first; Path=/; "
            "no-path-cookie=seventh; Domain=pathtest.com; "
            "path-cookie=eighth; Domain=pathtest.com; Path=/somepath; "
            "wrong-path-cookie=ninth; Domain=pathtest.com; Path=somepath;"
        )
        self.jar = CookieJar()
        self.jar.update_cookies(self.cookies_to_receive)

    def test_request_reply_with_same_url(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://pathtest.com/")
        
        self.assertEqual(
            set(cookies_received.keys()),
            {
                "unconstrained-cookie",
                "no-path-cookie",
                "path-cookie",
                "wrong-path-cookie",
            },
        )
        
        self.assertEqual(cookies_received["no-path-cookie"]["path"], "/")
        self.assertEqual(cookies_received["path-cookie"]["path"], "/somepath")
        self.assertEqual(cookies_received["wrong-path-cookie"]["path"], "/")

    def test_request_reply_with_different_url(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://different.com/")
        
        self.assertEqual(cookies_sent, SimpleCookie())
        self.assertEqual(len(cookies_received), 0)

    def test_request_reply_with_empty_url(self):
        with self.assertRaises(ValueError):
            self.request_reply_with_same_url("")

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