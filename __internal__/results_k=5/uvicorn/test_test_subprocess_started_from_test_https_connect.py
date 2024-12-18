import unittest
from unittest.mock import patch
from uvicorn.config import Config
from your_module import YourClass  # Replace with the actual module and class name

class TestYourClassCloseMethod(unittest.TestCase):

    def setUp(self):
        self.config = Config(app=None)  # Replace with actual app if needed
        self.instance = YourClass(self.config)

    def test_close_method_not_closed(self):
        self.instance.closed = False
        self.instance.close()
        self.assertTrue(self.instance.closed)

    def test_close_method_already_closed(self):
        self.instance.closed = True
        with self.assertRaises(AssertionError):
            self.instance.close()

    @patch('your_module.logging')  # Replace with actual logging module if needed
    def test_close_method_logging_called(self, mock_logging):
        self.instance.closed = False
        self.instance.close()
        mock_logging.info.assert_called_with("Instance closed.")

if __name__ == '__main__':
    unittest.main()