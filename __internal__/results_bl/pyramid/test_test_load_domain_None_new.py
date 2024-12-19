import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.i18n import Translations, Localizer

class TestLoadMethod(unittest.TestCase):

    def setUp(self):
        self.klass = self._getTargetClass()
        self.localedir = os.path.join(os.path.dirname(__file__), 'locales')

    def test_load_with_valid_value(self):
        self.klass.value = "Test Value"
        result = self.klass.load()
        self.assertEqual(result, "Test Value")

    def test_load_with_none_value(self):
        self.klass.value = None
        result = self.klass.load()
        self.assertIsNone(result)

    def test_load_with_empty_string(self):
        self.klass.value = ""
        result = self.klass.load()
        self.assertEqual(result, "")

    def test_load_with_translations(self):
        self.klass.value = Translations()
        result = self.klass.load()
        self.assertIsInstance(result, Translations)

    def test_load_with_localizer(self):
        self.klass.value = Localizer(DummyRequest())
        result = self.klass.load()
        self.assertIsInstance(result, Localizer)

    def _getTargetClass(self):
        from pyramid.i18n import Localizer
        return Localizer