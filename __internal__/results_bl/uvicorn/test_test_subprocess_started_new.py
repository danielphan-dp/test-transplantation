import socket
import unittest
from unittest.mock import patch
from uvicorn.config import Config

class TestCloseMethod(unittest.TestCase):
    def setUp(self):
        self.config = Config(app=None)
        self.config.closed = False

    def test_close_method_success(self):
        self.config.close()
        self.assertTrue(self.config.closed)

    def test_close_method_already_closed(self):
        self.config.closed = True
        with self.assertRaises(AssertionError):
            self.config.close()

    def test_close_method_multiple_calls(self):
        self.config.close()
        with self.assertRaises(AssertionError):
            self.config.close()

if __name__ == '__main__':
    unittest.main()