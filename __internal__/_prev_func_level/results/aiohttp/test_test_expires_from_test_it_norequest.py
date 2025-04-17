import unittest
from datetime import datetime, timedelta
from freezegun import freeze_time
from aiohttp import CookieJar
from http.cookies import SimpleCookie

class TestTimedRequest(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie("test-cookie=value; Path=/; Domain=example.com;")

    def timed_request(self, url: str, update_time: float, send_time: float):
        freeze_update_time = datetime.fromtimestamp(update_time) if not isinstance(update_time, int) else timedelta(seconds=update_time)
        freeze_send_time = datetime.fromtimestamp(send_time) if not isinstance(send_time, int) else timedelta(seconds=send_time)

        with freeze_time(freeze_update_time):
            self.jar.update_cookies(self.cookies_to_send)

        with freeze_time(freeze_send_time):
            cookies_sent = self.jar.filter_cookies(url)

        self.jar.clear()
        return cookies_sent

    def test_timed_request_with_past_and_future_times(self):
        ts_past = datetime(1970, 1, 1, tzinfo=datetime.timezone.utc).timestamp()
        ts_future = datetime(3000, 1, 1, tzinfo=datetime.timezone.utc).timestamp()

        cookies_sent = self.timed_request("http://example.com/", ts_past, ts_future)
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})

    def test_timed_request_with_same_time(self):
        ts_now = datetime.now(tz=datetime.timezone.utc).timestamp()
        cookies_sent = self.timed_request("http://example.com/", ts_now, ts_now)
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})

    def test_timed_request_with_invalid_url(self):
        ts_now = datetime.now(tz=datetime.timezone.utc).timestamp()
        with self.assertRaises(ValueError):
            self.timed_request("invalid-url", ts_now, ts_now)

    def test_timed_request_with_zero_update_time(self):
        ts_now = datetime.now(tz=datetime.timezone.utc).timestamp()
        cookies_sent = self.timed_request("http://example.com/", 0, ts_now)
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})

    def test_timed_request_with_negative_send_time(self):
        ts_now = datetime.now(tz=datetime.timezone.utc).timestamp()
        cookies_sent = self.timed_request("http://example.com/", ts_now, -1)
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})

if __name__ == '__main__':
    unittest.main()