import unittest
from unittest.mock import patch
from freezegun import freeze_time
from aiohttp import CookieJar
from http.cookies import SimpleCookie

class TestTimedRequest(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie("test-cookie=value; Path=/; Max-Age=3600;")
        self.jar.update_cookies(self.cookies_to_send)

    @freeze_time("2023-01-01 12:00:00")
    def test_timed_request_with_integer_times(self):
        cookies_sent = self.jar.filter_cookies("http://example.com/")
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})

    @freeze_time("2023-01-01 12:00:00")
    def test_timed_request_with_float_times(self):
        cookies_sent = self.jar.filter_cookies("http://example.com/")
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})

    @freeze_time("2023-01-01 12:00:00")
    def test_timed_request_with_future_update_time(self):
        cookies_sent = self.jar.filter_cookies("http://example.com/")
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})

    @freeze_time("2023-01-01 12:00:00")
    def test_timed_request_with_past_send_time(self):
        cookies_sent = self.jar.filter_cookies("http://example.com/")
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})

    @freeze_time("2023-01-01 12:00:00")
    def test_timed_request_no_cookies_sent(self):
        self.jar.clear()
        cookies_sent = self.jar.filter_cookies("http://example.com/")
        self.assertEqual(set(cookies_sent.keys()), set())

if __name__ == '__main__':
    unittest.main()