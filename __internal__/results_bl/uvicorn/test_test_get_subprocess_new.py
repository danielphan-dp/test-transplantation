import socket
import unittest
from unittest.mock import patch
from uvicorn._subprocess import SpawnProcess, get_subprocess
from uvicorn.config import Config

class TestCloseMethod(unittest.TestCase):
    def setUp(self):
        self.fdsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fd = self.fdsock.fileno()
        self.config = Config(app=None, fd=self.fd)
        self.config.load()
        self.process = get_subprocess(self.config, None, [self.fdsock])

    def tearDown(self):
        self.fdsock.close()

    def test_close_method_not_closed(self):
        self.assertFalse(self.process.closed)
        self.process.close()
        self.assertTrue(self.process.closed)

    def test_close_method_already_closed(self):
        self.process.close()
        with self.assertRaises(AssertionError):
            self.process.close()

    def test_close_method_edge_case(self):
        self.process.closed = True
        with self.assertRaises(AssertionError):
            self.process.close()