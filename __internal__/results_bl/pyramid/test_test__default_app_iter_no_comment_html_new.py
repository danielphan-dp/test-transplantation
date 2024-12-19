import unittest
from pyramid.httpexceptions import HTTPException

class TestGetTargetSubclass(unittest.TestCase):

    def test_get_target_subclass_default_values(self):
        cls = self._getTargetSubclass()
        exc = cls()
        self.assertEqual(exc.code, '200')
        self.assertEqual(exc.title, 'OK')
        self.assertEqual(exc.explanation, 'explanation')
        self.assertFalse(exc.empty_body)

    def test_get_target_subclass_custom_values(self):
        code = '404'
        title = 'Not Found'
        explanation = 'The requested resource was not found.'
        empty_body = True
        cls = self._getTargetSubclass(code, title, explanation, empty_body)
        exc = cls()
        self.assertEqual(exc.code, code)
        self.assertEqual(exc.title, title)
        self.assertEqual(exc.explanation, explanation)
        self.assertTrue(exc.empty_body)

    def test_get_target_subclass_empty_body(self):
        cls = self._getTargetSubclass(empty_body=True)
        exc = cls()
        self.assertTrue(exc.empty_body)

    def test_get_target_subclass_non_default_code(self):
        cls = self._getTargetSubclass(code='500')
        exc = cls()
        self.assertEqual(exc.code, '500')

    def test_get_target_subclass_non_default_title(self):
        cls = self._getTargetSubclass(title='Internal Server Error')
        exc = cls()
        self.assertEqual(exc.title, 'Internal Server Error')

    def test_get_target_subclass_non_default_explanation(self):
        cls = self._getTargetSubclass(explanation='An unexpected error occurred.')
        exc = cls()
        self.assertEqual(exc.explanation, 'An unexpected error occurred.')