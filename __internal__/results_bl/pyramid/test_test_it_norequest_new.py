import unittest
from pyramid.scripting import get_root
from pyramid.threadlocal import manager

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.registry = self._makeRegistry([DummyFactory, None, DummyFactory])
        self.info = self._callFUT(registry=self.registry)
        self.root, self.closer, self.request = self.info['root'], self.info['closer'], self.info['request']
        self.manager = manager

    def test_get_method_with_valid_name(self):
        pushed = self.manager.get('valid_name')
        self.assertEqual(pushed['registry'], self.registry)
        self.assertEqual(pushed['request'].registry, self.registry)

    def test_get_method_with_none_name(self):
        pushed = self.manager.get(None)
        self.assertIsNone(pushed)

    def test_get_method_with_empty_string(self):
        pushed = self.manager.get('')
        self.assertIsNone(pushed)

    def test_get_method_with_unregistered_name(self):
        pushed = self.manager.get('unregistered_name')
        self.assertIsNone(pushed)

    def tearDown(self):
        self.closer()