import os.path
import unittest
from pyramid.testing import cleanUp
from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError
from pyramid.config.assets import PackageAssetSource
from tests.test_config.pkgs.asset import DummyAssetSource, DummyOverride, DummyPackage

class TestGetFilename(unittest.TestCase):

    def setUp(self):
        self.source = DummyAssetSource(filename='foo.pt')
        self.overrides = [DummyOverride(None), DummyOverride((self.source, ''))]
        self.package = DummyPackage('package')
        self.po = self._makeOne(self.package)
        self.po.overrides = self.overrides

    def _makeOne(self, package):
        return package  # Replace with actual instantiation logic

    def test_get_filename_valid_resource(self):
        result = self.po.get_filename('whatever')
        self.assertEqual(result, 'foo.pt')
        self.assertEqual(self.source.resource_name, '')

    def test_get_filename_empty_resource_name(self):
        result = self.po.get_filename('')
        self.assertEqual(result, 'foo.pt')

    def test_get_filename_non_existent_resource(self):
        result = self.po.get_filename('non_existent')
        self.assertIsNone(result)  # Assuming the method returns None for non-existent resources

    def test_get_filename_with_different_source(self):
        another_source = DummyAssetSource(filename='bar.pt')
        self.po.overrides.append(DummyOverride((another_source, '')))
        result = self.po.get_filename('different_resource')
        self.assertEqual(result, 'bar.pt')

    def test_get_filename_with_none_resource(self):
        with self.assertRaises(TypeError):
            self.po.get_filename(None)

    def tearDown(self):
        cleanUp()