import unittest
from pyramid.scripting import closer
from pyramid.threadlocal import manager

class TestCloserFunction(unittest.TestCase):

    def setUp(self):
        self.original_closer_called = manager.get().get('closer_called', [False])
        self.original_closer = closer

    def tearDown(self):
        manager.get()['closer_called'] = self.original_closer_called

    def test_closer_called(self):
        closer()
        self.assertTrue(self.original_closer_called[0])

    def test_closer_not_called(self):
        self.assertFalse(self.original_closer_called[0])

    def test_closer_multiple_calls(self):
        closer()
        closer()
        self.assertTrue(self.original_closer_called[0])

    def test_closer_state_after_call(self):
        closer()
        self.assertEqual(manager.get()['closer_called'], [True])