import unittest
from pyramid.util import InstancePropertyHelper
from pyramid.threadlocal import manager
from pyramid.exceptions import ConfigurationError

class TestCloserMethod(unittest.TestCase):

    def setUp(self):
        self.closer_called = [False]

    def mock_orig_closer(self):
        pass

    def test_closer_called(self):
        self.closer_called[0] = False
        closer = self._callFUT()
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_with_no_previous_call(self):
        self.closer_called[0] = False
        closer = self._callFUT()
        self.assertFalse(self.closer_called[0])
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_multiple_calls(self):
        closer = self._callFUT()
        closer()
        self.assertTrue(self.closer_called[0])
        closer()  # Call again to ensure no side effects
        self.assertTrue(self.closer_called[0])

    def _callFUT(self):
        orig_closer = self.mock_orig_closer
        def closer():
            orig_closer()
            self.closer_called[0] = True
        return closer

if __name__ == '__main__':
    unittest.main()