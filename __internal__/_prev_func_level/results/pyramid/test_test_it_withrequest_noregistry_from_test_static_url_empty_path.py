import unittest
from pyramid.scripting import closer
from pyramid.threadlocal import manager

class TestCloserFunction(unittest.TestCase):

    def setUp(self):
        self.closer_called = [False]
        self.orig_closer = manager.get_closer
        manager.get_closer = self.mock_closer

    def tearDown(self):
        manager.get_closer = self.orig_closer

    def mock_closer(self):
        self.closer_called[0] = True

    def test_closer_function_called(self):
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_function_idempotency(self):
        closer()
        self.closer_called[0] = False
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_function_state(self):
        self.assertFalse(self.closer_called[0])
        closer()
        self.assertTrue(self.closer_called[0])