import unittest
from unittest.mock import Mock
from uvicorn.config import Config
from uvicorn._subprocess import SpawnProcess

class TestCloseMethod(unittest.TestCase):
    def setUp(self):
        self.config = Config(app=Mock())
        self.instance = Mock()
        self.instance.closed = False

    def test_close_method_success(self):
        self.instance.close()
        self.assertTrue(self.instance.closed)

    def test_close_method_already_closed(self):
        self.instance.closed = True
        with self.assertRaises(AssertionError):
            self.instance.close()

    def test_close_method_multiple_calls(self):
        self.instance.close()
        with self.assertRaises(AssertionError):
            self.instance.close()

if __name__ == '__main__':
    unittest.main()