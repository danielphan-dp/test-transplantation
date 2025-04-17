import unittest
from pyramid.scripting import closer
from pyramid.threadlocal import manager

class TestCloserFunction(unittest.TestCase):

    def setUp(self):
        self.closer_called = [False]

    def test_closer_function_called(self):
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_function_multiple_calls(self):
        closer()
        self.assertTrue(self.closer_called[0])
        closer()  # Call again to ensure it doesn't affect the state
        self.assertTrue(self.closer_called[0])

    def test_closer_function_state(self):
        self.closer_called[0] = False
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_function_with_registry(self):
        registry = self._makeRegistry([DummyFactory, None, DummyFactory])
        info = self._callFUT(registry=registry)
        root, closer, request = info['root'], info['closer'], info['request']
        pushed = manager.get()
        self.assertEqual(pushed['registry'], registry)
        self.assertEqual(pushed['request'].registry, registry)
        self.assertEqual(root.a, (pushed['request'],))
        closer()
        self.assertEqual(self.default, manager.get())
        self.assertEqual(request.context, root)

if __name__ == '__main__':
    unittest.main()