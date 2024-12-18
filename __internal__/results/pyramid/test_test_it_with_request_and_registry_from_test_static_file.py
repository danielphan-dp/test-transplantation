import unittest
from pyramid.scripting import closer
from pyramid.threadlocal import manager

class TestCloserMethod(unittest.TestCase):

    def setUp(self):
        self.original_closer_called = manager.get()
        self.closer_called = [False]

    def test_closer_called(self):
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_not_called_initially(self):
        self.assertFalse(self.closer_called[0])

    def test_closer_functionality(self):
        closer()
        self.assertEqual(self.original_closer_called, manager.get())

    def test_closer_multiple_calls(self):
        closer()
        self.assertTrue(self.closer_called[0])
        closer()  # Call again to ensure no side effects
        self.assertTrue(self.closer_called[0])

    def tearDown(self):
        self.closer_called[0] = False
        manager.set(self.original_closer_called)