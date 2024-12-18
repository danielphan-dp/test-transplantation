import unittest
from unittest.mock import patch
from freezegun import freeze_time
from aiohttp import CookieJar
from http.cookies import SimpleCookie

class TestTimedRequest(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie("test-cookie=value; Path=/; Max-Age=3600")
        self.jar.update_cookies(self.cookies_to_send)

    @freeze_time("2023-01-01 12:00:00")
    def test_timed_request_with_integer_times(self):
        cookies_sent = self.timed_request("http://example.com/", 1000, 2000)
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})

    @freeze_time("2023-01-01 12:00:00")
    def test_timed_request_with_datetime_times(self):
        update_time = datetime.datetime(2023, 1, 1, 12, 0, 0)
        send_time = datetime.datetime(2023, 1, 1, 12, 30, 0)
        cookies_sent = self.timed_request("http://example.com/", update_time, send_time)
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})

    @freeze_time("2023-01-01 12:00:00")
    def test_timed_request_with_no_cookies_sent(self):
        self.jar.clear()
        cookies_sent = self.timed_request("http://example.com/", 1000, 2000)
        self.assertEqual(cookies_sent, {})

    @freeze_time("2023-01-01 12:00:00")
    def test_timed_request_with_expired_cookie(self):
        expired_cookie = SimpleCookie("expired-cookie=value; Path=/; Max-Age=0")
        self.jar.update_cookies(expired_cookie)
        cookies_sent = self.timed_request("http://example.com/", 1000, 2000)
        self.assertEqual(cookies_sent, {})

    @freeze_time("2023-01-01 12:00:00")
    def test_timed_request_with_multiple_cookies(self):
        multiple_cookies = SimpleCookie("cookie1=value1; Path=/; Max-Age=3600; cookie2=value2; Path=/; Max-Age=3600")
        self.jar.update_cookies(multiple_cookies)
        cookies_sent = self.timed_request("http://example.com/", 1000, 2000)
        self.assertEqual(set(cookies_sent.keys()), {"cookie1", "cookie2"})