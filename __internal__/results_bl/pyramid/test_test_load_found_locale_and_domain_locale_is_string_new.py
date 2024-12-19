import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.i18n import Localizer

class TestLoadMethod(unittest.TestCase):

    def _getTargetClass(self):
        return Localizer

    def test_load_returns_value(self):
        klass = self._getTargetClass()
        localizer = klass('de', domain='deformsite')
        localizer.value = 'test_value'
        result = localizer.load()
        self.assertEqual(result, 'test_value')

    def test_load_with_none_value(self):
        klass = self._getTargetClass()
        localizer = klass('de', domain='deformsite')
        localizer.value = None
        result = localizer.load()
        self.assertIsNone(result)

    def test_load_with_empty_string(self):
        klass = self._getTargetClass()
        localizer = klass('de', domain='deformsite')
        localizer.value = ''
        result = localizer.load()
        self.assertEqual(result, '')

    def test_load_with_different_locale(self):
        klass = self._getTargetClass()
        localizer = klass('fr', domain='deformsite')
        localizer.value = 'valeur_test'
        result = localizer.load()
        self.assertEqual(result, 'valeur_test')

    def test_load_with_unset_value(self):
        klass = self._getTargetClass()
        localizer = klass('de', domain='deformsite')
        del localizer.value
        with self.assertRaises(AttributeError):
            localizer.load()