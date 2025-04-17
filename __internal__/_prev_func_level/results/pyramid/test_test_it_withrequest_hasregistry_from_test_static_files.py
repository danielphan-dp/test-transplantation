import unittest
from pyramid.scripting import closer
from pyramid.threadlocal import manager

class TestCloserMethod(unittest.TestCase):

    def setUp(self):
        self.manager = manager
        self.closer_called = [False]

    def test_closer_called(self):
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_state_after_call(self):
        closer()
        self.assertEqual(self.manager.get(), None)

    def test_closer_multiple_calls(self):
        closer()
        self.assertTrue(self.closer_called[0])
        self.closer_called[0] = False
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_with_no_registry(self):
        self.manager.push({'request': None, 'registry': None})
        closer()
        self.assertIsNone(self.manager.get()['registry'])

    def test_closer_with_different_context(self):
        self.manager.push({'request': 'dummy_request', 'registry': 'dummy_registry'})
        closer()
        self.assertEqual(self.manager.get()['request'], 'dummy_request')
        self.assertEqual(self.manager.get()['registry'], 'dummy_registry')

if __name__ == '__main__':
    unittest.main()