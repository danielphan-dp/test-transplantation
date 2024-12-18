import asyncio
import datetime
import unittest
from http.cookies import BaseCookie
from unittest.mock import patch
from freezegun import freeze_time
from yarl import URL
from aiohttp import CookieJar

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = {'shared-cookie': 'value1', 'expires-cookie': 'value2'}
        self.jar.update_cookies(self.cookies_to_send)

    @freeze_time("1975-01-01")
    def test_timed_request_with_past_update_time(self):
        cookies_sent = self.jar.timed_request("http://test.com/", 0, 0)
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie", "expires-cookie"})

    @freeze_time("2030-01-01")
    def test_timed_request_with_future_send_time(self):
        cookies_sent = self.jar.timed_request("http://test.com/", 0, 0)
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie"})

    @freeze_time("1975-01-01")
    def test_timed_request_with_negative_update_time(self):
        cookies_sent = self.jar.timed_request("http://test.com/", -1, -1)
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie", "expires-cookie"})

    @freeze_time("2030-01-01")
    def test_timed_request_with_large_send_time(self):
        future_time = (datetime.datetime.now() + datetime.timedelta(days=365)).timestamp()
        cookies_sent = self.jar.timed_request("http://test.com/", 0, future_time)
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie"})

    @freeze_time("1975-01-01")
    def test_timed_request_with_invalid_url(self):
        with self.assertRaises(ValueError):
            self.jar.timed_request("invalid-url", 0, 0)

    @freeze_time("1975-01-01")
    def test_timed_request_with_empty_url(self):
        cookies_sent = self.jar.timed_request("", 0, 0)
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie", "expires-cookie"})