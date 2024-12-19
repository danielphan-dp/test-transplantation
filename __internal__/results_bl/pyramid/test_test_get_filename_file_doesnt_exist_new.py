import os.path
import unittest
from pyramid.testing import cleanUp
from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError
from pyramid.config.assets import PackageAssetSource
from tests.test_config.pkgs.asset import DummyAssetSource, DummyOverride, DummyPackage

class TestGetFilename(unittest.TestCase):

    def setUp(self):
        self.package = DummyPackage('package')
        self.po = self._makeOne(self.package)

    def test_get_filename_file_exists(self):
        source = DummyAssetSource(filename='existing_file.txt')
        overrides = [DummyOverride((source, 'existing_file.txt'))]
        self.po.overrides = overrides
        self.assertEqual(self.po.get_filename('existing_file.txt'), 'existing_file.txt')
        self.assertEqual(source.resource_name, 'existing_file.txt')

    def test_get_filename_with_different_resource_name(self):
        source = DummyAssetSource(filename='another_file.txt')
        overrides = [DummyOverride((source, 'different_resource'))]
        self.po.overrides = overrides
        self.assertEqual(self.po.get_filename('different_resource'), 'another_file.txt')
        self.assertEqual(source.resource_name, 'different_resource')

    def test_get_filename_no_overrides(self):
        self.po.overrides = []
        self.assertEqual(self.po.get_filename('whatever'), None)

    def test_get_filename_invalid_resource_name(self):
        source = DummyAssetSource(filename=None)
        overrides = [DummyOverride((source, 'invalid_resource'))]
        self.po.overrides = overrides
        self.assertEqual(self.po.get_filename('invalid_resource'), None)
        self.assertEqual(source.resource_name, 'invalid_resource')

    def test_get_filename_multiple_overrides(self):
        source1 = DummyAssetSource(filename='file1.txt')
        source2 = DummyAssetSource(filename='file2.txt')
        overrides = [
            DummyOverride((source1, 'file1')),
            DummyOverride((source2, 'file2'))
        ]
        self.po.overrides = overrides
        self.assertEqual(self.po.get_filename('file1'), 'file1.txt')
        self.assertEqual(self.po.get_filename('file2'), 'file2.txt')
        self.assertEqual(source1.resource_name, 'file1')
        self.assertEqual(source2.resource_name, 'file2')

    def _makeOne(self, package):
        return package  # Replace with actual instantiation logic if needed

    def tearDown(self):
        cleanUp()