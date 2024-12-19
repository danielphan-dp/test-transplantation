import unittest
from pyramid.httpexceptions import HTTPException

class TestGetTargetSubclass(unittest.TestCase):

    def test_get_target_subclass_with_empty_body(self):
        cls = self._getTargetSubclass(empty_body=True)
        exc = cls()
        self.assertTrue(exc.empty_body)

    def test_get_target_subclass_with_custom_code(self):
        custom_code = '404'
        cls = self._getTargetSubclass(code=custom_code)
        exc = cls()
        self.assertEqual(exc.code, custom_code)

    def test_get_target_subclass_with_custom_title(self):
        custom_title = 'Not Found'
        cls = self._getTargetSubclass(title=custom_title)
        exc = cls()
        self.assertEqual(exc.title, custom_title)

    def test_get_target_subclass_with_custom_explanation(self):
        custom_explanation = 'The resource was not found.'
        cls = self._getTargetSubclass(explanation=custom_explanation)
        exc = cls()
        self.assertEqual(exc.explanation, custom_explanation)

    def test_get_target_subclass_with_invalid_code(self):
        with self.assertRaises(HTTPException):
            cls = self._getTargetSubclass(code='invalid_code')
            exc = cls()
            self.assertEqual(exc.code, 'invalid_code')

    def test_get_target_subclass_with_none_values(self):
        cls = self._getTargetSubclass(code=None, title=None, explanation=None)
        exc = cls()
        self.assertIsNone(exc.code)
        self.assertIsNone(exc.title)
        self.assertIsNone(exc.explanation)