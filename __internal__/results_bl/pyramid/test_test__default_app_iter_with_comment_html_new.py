import unittest
from pyramid.httpexceptions import HTTPException

class TestGetTargetSubclass(unittest.TestCase):

    def test_get_target_subclass_with_default_values(self):
        cls = self._getTargetSubclass()
        exc = cls()
        self.assertEqual(exc.code, '200')
        self.assertEqual(exc.title, 'OK')
        self.assertEqual(exc.explanation, 'explanation')
        self.assertFalse(exc.empty_body)

    def test_get_target_subclass_with_custom_values(self):
        code = '404'
        title = 'Not Found'
        explanation = 'The requested resource was not found.'
        exc = self._getTargetSubclass(code=code, title=title, explanation=explanation)()
        self.assertEqual(exc.code, code)
        self.assertEqual(exc.title, title)
        self.assertEqual(exc.explanation, explanation)

    def test_get_target_subclass_with_empty_body(self):
        exc = self._getTargetSubclass(empty_body=True)()
        self.assertTrue(exc.empty_body)

    def test_get_target_subclass_with_invalid_code(self):
        with self.assertRaises(ValueError):
            self._getTargetSubclass(code='invalid_code')()

    def test_get_target_subclass_with_none_title(self):
        exc = self._getTargetSubclass(title=None)()
        self.assertIsNone(exc.title)

    def test_get_target_subclass_with_none_explanation(self):
        exc = self._getTargetSubclass(explanation=None)()
        self.assertIsNone(exc.explanation)