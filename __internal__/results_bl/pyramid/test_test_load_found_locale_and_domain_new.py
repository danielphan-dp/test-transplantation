import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.i18n import Localizer

class TestLoadMethod(unittest.TestCase):

    def setUp(self):
        self.localizer = Localizer('en')

    def test_load_returns_value(self):
        result = self.localizer.load()
        self.assertEqual(result, self.localizer.value)

    def test_load_with_different_locales(self):
        locales = ['fr', 'es']
        self.localizer.locales = locales
        result = self.localizer.load()
        self.assertEqual(result, self.localizer.value)

    def test_load_empty_locale(self):
        self.localizer.locales = []
        result = self.localizer.load()
        self.assertEqual(result, self.localizer.value)

    def test_load_invalid_locale(self):
        self.localizer.locales = ['invalid_locale']
        result = self.localizer.load()
        self.assertEqual(result, self.localizer.value)

    def test_load_none_locale(self):
        self.localizer.locales = None
        result = self.localizer.load()
        self.assertEqual(result, self.localizer.value)