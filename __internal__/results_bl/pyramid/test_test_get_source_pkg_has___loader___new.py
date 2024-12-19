import os.path
import unittest
from pyramid.testing import cleanUp
from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError
from pyramid.config.assets import PackageAssetSource

class TestGetSource(unittest.TestCase):

    def setUp(self):
        self.package = DummyPackage('package')
        self.loader = self.package.__loader__ = DummyLoader()
        self.po = self._makeOne(self.package)

    def test_get_source_valid_fullname(self):
        self.assertEqual(self.po.get_source('valid_name'), 'def foo():\n    pass')
        self.assertEqual(self.loader._got_source, 'valid_name')

    def test_get_source_empty_fullname(self):
        with self.assertRaises(ValueError):
            self.po.get_source('')

    def test_get_source_none_fullname(self):
        with self.assertRaises(TypeError):
            self.po.get_source(None)

    def test_get_source_special_characters(self):
        self.assertEqual(self.po.get_source('name_with_special_chars!@#'), 'def foo():\n    pass')
        self.assertEqual(self.loader._got_source, 'name_with_special_chars!@#')

    def test_get_source_numeric_fullname(self):
        self.assertEqual(self.po.get_source('12345'), 'def foo():\n    pass')
        self.assertEqual(self.loader._got_source, '12345')

    def test_get_source_long_fullname(self):
        long_name = 'a' * 1000
        self.assertEqual(self.po.get_source(long_name), 'def foo():\n    pass')
        self.assertEqual(self.loader._got_source, long_name)

    def test_get_source_repeated_calls(self):
        self.po.get_source('first_call')
        self.assertEqual(self.loader._got_source, 'first_call')
        self.po.get_source('second_call')
        self.assertEqual(self.loader._got_source, 'second_call')