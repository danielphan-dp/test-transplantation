import unittest
from pyramid.httpexceptions import HTTPException

class TestGetTargetSubclass(unittest.TestCase):

    def test_default_values(self):
        cls = self._getTargetSubclass()
        exc = cls()
        self.assertEqual(exc.code, '200')
        self.assertEqual(exc.title, 'OK')
        self.assertEqual(exc.explanation, 'explanation')
        self.assertFalse(exc.empty_body)

    def test_custom_values(self):
        code = '404'
        title = 'Not Found'
        explanation = 'The requested resource was not found.'
        cls = self._getTargetSubclass(code=code, title=title, explanation=explanation)
        exc = cls()
        self.assertEqual(exc.code, code)
        self.assertEqual(exc.title, title)
        self.assertEqual(exc.explanation, explanation)

    def test_empty_body(self):
        cls = self._getTargetSubclass(empty_body=True)
        exc = cls()
        self.assertTrue(exc.empty_body)

    def test_invalid_code(self):
        with self.assertRaises(ValueError):
            self._getTargetSubclass(code='invalid')

    def test_edge_case_empty_title(self):
        cls = self._getTargetSubclass(title='')
        exc = cls()
        self.assertEqual(exc.title, '')

    def test_edge_case_empty_explanation(self):
        cls = self._getTargetSubclass(explanation='')
        exc = cls()
        self.assertEqual(exc.explanation, '')