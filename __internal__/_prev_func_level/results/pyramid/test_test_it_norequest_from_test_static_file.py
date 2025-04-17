import unittest
from pyramid.scripting import closer
from pyramid.threadlocal import manager

class TestCloserFunction(unittest.TestCase):

    def setUp(self):
        self.original_closer_called = False

    def mock_closer(self):
        self.original_closer_called = True

    def test_closer_called(self):
        global closer_called
        closer_called = [False]
        original_closer = closer
        closer = self.mock_closer
        closer()
        self.assertTrue(closer_called[0])
        closer = original_closer

    def test_closer_no_request(self):
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

    def test_closer_edge_case(self):
        global closer_called
        closer_called = [False]
        # Simulate an edge case where closer is called multiple times
        for _ in range(3):
            closer()
        self.assertTrue(closer_called[0])

    def test_closer_with_exception(self):
        global closer_called
        closer_called = [False]
        def faulty_closer():
            raise Exception("Closer failed")
        
        original_closer = closer
        closer = faulty_closer
        with self.assertRaises(Exception):
            closer()
        closer = original_closer

if __name__ == '__main__':
    unittest.main()