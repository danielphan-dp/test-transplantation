import unittest
from pyramid.scripting import closer

class TestCloserMethod(unittest.TestCase):

    def setUp(self):
        self.closer_called = [False]

    def test_closer_called(self):
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_not_called_initially(self):
        self.assertFalse(self.closer_called[0])

    def test_closer_multiple_calls(self):
        closer()
        self.assertTrue(self.closer_called[0])
        self.closer_called[0] = False  # Reset for next call
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_state_after_call(self):
        closer()
        self.assertTrue(self.closer_called[0])
        # Simulate some state change
        self.closer_called[0] = False
        self.assertFalse(self.closer_called[0])