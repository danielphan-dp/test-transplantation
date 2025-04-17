import unittest
from unittest.mock import Mock
from uvicorn.config import Config
from uvicorn._subprocess import SpawnProcess

class TestCloseMethod(unittest.TestCase):
    def setUp(self):
        self.config = Config(app=Mock())
        self.process = SpawnProcess(self.config)

    def test_close_method_not_closed(self):
        self.process.closed = False
        self.process.close()
        self.assertTrue(self.process.closed)

    def test_close_method_already_closed(self):
        self.process.closed = True
        with self.assertRaises(AssertionError):
            self.process.close()

    def test_close_method_multiple_calls(self):
        self.process.closed = False
        self.process.close()
        self.assertTrue(self.process.closed)
        with self.assertRaises(AssertionError):
            self.process.close()

if __name__ == '__main__':
    unittest.main()