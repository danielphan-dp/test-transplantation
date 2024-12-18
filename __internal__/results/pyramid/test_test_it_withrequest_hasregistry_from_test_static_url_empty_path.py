import unittest
from pyramid.scripting import closer
from pyramid.threadlocal import manager

class TestCloserMethod(unittest.TestCase):

    def setUp(self):
        self.manager = manager

    def test_closer_called(self):
        closer_called = [False]
        def orig_closer():
            closer_called[0] = True
        
        closer()
        self.assertTrue(closer_called[0])

    def test_closer_state(self):
        closer_called = [False]
        def orig_closer():
            closer_called[0] = True
        
        closer()
        self.assertTrue(closer_called[0])
        self.manager.push({'request': 'dummy_request'})
        self.assertEqual(self.manager.get()['request'], 'dummy_request')
        closer()
        self.assertIsNone(self.manager.get())

    def test_closer_with_no_request(self):
        closer_called = [False]
        def orig_closer():
            closer_called[0] = True
        
        self.manager.push({})
        closer()
        self.assertTrue(closer_called[0])
        self.assertIsNone(self.manager.get())

    def test_closer_multiple_calls(self):
        closer_called = [False]
        def orig_closer():
            closer_called[0] = True
        
        closer()
        self.assertTrue(closer_called[0])
        closer_called[0] = False
        closer()
        self.assertTrue(closer_called[0])

if __name__ == '__main__':
    unittest.main()