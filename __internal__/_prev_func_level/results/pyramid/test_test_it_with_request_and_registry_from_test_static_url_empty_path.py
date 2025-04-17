import unittest
from pyramid.scripting import closer
from pyramid.threadlocal import manager

class TestCloserFunction(unittest.TestCase):

    def setUp(self):
        self.closer_called = [False]

    def test_closer_function_called(self):
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_function_state(self):
        closer()
        self.assertTrue(self.closer_called[0])
        # Reset state and call again
        self.closer_called[0] = False
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_function_with_manager(self):
        request = DummyRequest({})
        registry = request.registry = self._makeRegistry()
        info = self._callFUT(request=request, registry=registry)
        root, closer, root = info['root'], info['closer'], info['root']
        pushed = manager.get()
        self.assertEqual(pushed['request'], request)
        self.assertEqual(pushed['registry'], registry)
        self.assertEqual(pushed['request'].registry, registry)
        self.assertEqual(root.a, (request,))
        closer()
        self.assertEqual(self.default, manager.get())
        self.assertEqual(request.context, root)

    def test_closer_function_edge_case(self):
        # Simulate an edge case where closer is called multiple times
        for _ in range(5):
            closer()
        self.assertTrue(self.closer_called[0])

if __name__ == '__main__':
    unittest.main()