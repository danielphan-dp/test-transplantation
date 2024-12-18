import unittest
from unittest.mock import patch
from uvicorn.config import Config
from uvicorn._subprocess import SpawnProcess

class TestCloseMethod(unittest.TestCase):

    def setUp(self):
        self.config = Config(app=None)
        self.process = SpawnProcess(self.config)

    def test_close_method_not_closed(self):
        self.process.closed = False
        self.process.close()
        self.assertTrue(self.process.closed)

    def test_close_method_already_closed(self):
        self.process.closed = True
        with self.assertRaises(AssertionError):
            self.process.close()

    @patch('uvicorn._subprocess.SpawnProcess.close')
    def test_close_method_called(self, mock_close):
        self.process.closed = False
        self.process.close()
        mock_close.assert_called_once()

if __name__ == '__main__':
    unittest.main()