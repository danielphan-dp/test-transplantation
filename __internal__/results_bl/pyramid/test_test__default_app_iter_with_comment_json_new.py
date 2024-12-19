import unittest
from pyramid.httpexceptions import HTTPException

class TestGetTargetSubclass(unittest.TestCase):

    def test_get_target_subclass_with_custom_code(self):
        cls = self._getTargetSubclass(code='404')
        exc = cls()
        self.assertEqual(exc.code, '404')
        self.assertEqual(exc.title, 'OK')

    def test_get_target_subclass_with_empty_body(self):
        cls = self._getTargetSubclass(empty_body=True)
        exc = cls()
        self.assertTrue(exc.empty_body)

    def test_get_target_subclass_with_custom_explanation(self):
        custom_explanation = 'Custom explanation'
        cls = self._getTargetSubclass(explanation=custom_explanation)
        exc = cls()
        self.assertEqual(exc.explanation, custom_explanation)

    def test_get_target_subclass_with_different_title(self):
        cls = self._getTargetSubclass(title='Not Found')
        exc = cls()
        self.assertEqual(exc.title, 'Not Found')

    def test_get_target_subclass_with_invalid_code(self):
        with self.assertRaises(HTTPException):
            cls = self._getTargetSubclass(code='invalid_code')
            exc = cls()