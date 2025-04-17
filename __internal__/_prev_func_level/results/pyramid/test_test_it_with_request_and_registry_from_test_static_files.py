import unittest
from pyramid.scripting import closer
from pyramid.threadlocal import manager

class TestCloserMethod(unittest.TestCase):

    def setUp(self):
        self.closer_called = [False]

    def test_closer_called(self):
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_multiple_calls(self):
        closer()
        self.assertTrue(self.closer_called[0])
        self.closer_called[0] = False
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_state(self):
        self.assertFalse(self.closer_called[0])
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_with_manager(self):
        request = DummyRequest({})
        registry = request.registry = self._makeRegistry()
        info = self._callFUT(request=request, registry=registry)
        root, closer, root = info['root'], info['closer'], info['root']
        pushed = manager.get()
        self.assertEqual(pushed['request'], request)
        self.assertEqual(pushed['registry'], registry)
        closer()
        self.assertEqual(self.default, manager.get())
        self.assertEqual(request.context, root)

if __name__ == '__main__':
    unittest.main()