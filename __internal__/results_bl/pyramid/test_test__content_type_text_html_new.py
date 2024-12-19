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
        cls = self._getTargetSubclass(code=code, title=title, explanation=explanation, empty_body=True)
        exc = cls()
        self.assertEqual(exc.code, code)
        self.assertEqual(exc.title, title)
        self.assertEqual(exc.explanation, explanation)
        self.assertTrue(exc.empty_body)

    def test_empty_body_false(self):
        cls = self._getTargetSubclass(empty_body=False)
        exc = cls()
        self.assertFalse(exc.empty_body)

    def test_empty_body_true(self):
        cls = self._getTargetSubclass(empty_body=True)
        exc = cls()
        self.assertTrue(exc.empty_body)

    def test_invalid_code(self):
        with self.assertRaises(HTTPException):
            cls = self._getTargetSubclass(code='invalid')
            exc = cls()