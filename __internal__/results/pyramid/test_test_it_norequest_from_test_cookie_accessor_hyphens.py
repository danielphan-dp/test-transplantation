import unittest
from pyramid.scripting import get_root
from pyramid.threadlocal import manager

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.registry = self._makeRegistry([DummyFactory, None, DummyFactory])
        self.manager = manager

    def test_get_method_with_valid_name(self):
        name = "test_cookie"
        result = self.manager.get(name)
        self.assertEqual(result, self.manager.cookie)

    def test_get_method_with_invalid_name(self):
        name = "invalid_cookie"
        result = self.manager.get(name)
        self.assertIsNone(result)

    def test_get_method_with_empty_name(self):
        name = ""
        result = self.manager.get(name)
        self.assertIsNone(result)

    def test_get_method_with_none_name(self):
        name = None
        result = self.manager.get(name)
        self.assertIsNone(result)

    def test_get_method_registry_integrity(self):
        pushed = self.manager.get()
        self.assertEqual(pushed['registry'], self.registry)

    def test_get_method_request_integrity(self):
        pushed = self.manager.get()
        self.assertEqual(pushed['request'].registry, self.registry)

    def test_get_method_closer_functionality(self):
        pushed = self.manager.get()
        closer = pushed['closer']
        closer()
        self.assertEqual(self.default, self.manager.get())

    def test_get_method_root_context(self):
        pushed = self.manager.get()
        root = pushed['root']
        self.assertEqual(root.a, (pushed['request'],))