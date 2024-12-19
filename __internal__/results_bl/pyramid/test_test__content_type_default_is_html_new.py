import unittest
from pyramid.httpexceptions import HTTPException

class TestGetTargetSubclass(unittest.TestCase):

    def test_get_target_subclass_with_custom_code(self):
        cls = self._getTargetSubclass(code='404')
        exc = cls()
        self.assertEqual(exc.code, '404')

    def test_get_target_subclass_with_custom_title(self):
        cls = self._getTargetSubclass(title='Not Found')
        exc = cls()
        self.assertEqual(exc.title, 'Not Found')

    def test_get_target_subclass_with_custom_explanation(self):
        cls = self._getTargetSubclass(explanation='The resource was not found.')
        exc = cls()
        self.assertEqual(exc.explanation, 'The resource was not found.')

    def test_get_target_subclass_with_empty_body(self):
        cls = self._getTargetSubclass(empty_body=True)
        exc = cls()
        self.assertTrue(exc.empty_body)

    def test_get_target_subclass_with_default_values(self):
        cls = self._getTargetSubclass()
        exc = cls()
        self.assertEqual(exc.code, '200')
        self.assertEqual(exc.title, 'OK')
        self.assertEqual(exc.explanation, 'explanation')
        self.assertFalse(exc.empty_body)

    def test_get_target_subclass_with_invalid_code(self):
        with self.assertRaises(ValueError):
            self._getTargetSubclass(code='invalid')

    def test_get_target_subclass_with_none_title(self):
        cls = self._getTargetSubclass(title=None)
        exc = cls()
        self.assertIsNone(exc.title)

    def test_get_target_subclass_with_none_explanation(self):
        cls = self._getTargetSubclass(explanation=None)
        exc = cls()
        self.assertIsNone(exc.explanation)