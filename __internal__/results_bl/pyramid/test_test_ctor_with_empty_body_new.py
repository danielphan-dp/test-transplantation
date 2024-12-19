import unittest
from pyramid.httpexceptions import HTTPException

class TestGetTargetSubclass(unittest.TestCase):

    def test_ctor_with_default_values(self):
        cls = self._getTargetSubclass()
        exc = cls()
        self.assertEqual(exc.code, '200')
        self.assertEqual(exc.title, 'OK')
        self.assertEqual(exc.explanation, 'explanation')
        self.assertFalse(exc.empty_body)

    def test_ctor_with_custom_code(self):
        cls = self._getTargetSubclass(code='404')
        exc = cls()
        self.assertEqual(exc.code, '404')

    def test_ctor_with_custom_title(self):
        cls = self._getTargetSubclass(title='Not Found')
        exc = cls()
        self.assertEqual(exc.title, 'Not Found')

    def test_ctor_with_custom_explanation(self):
        cls = self._getTargetSubclass(explanation='Resource not found')
        exc = cls()
        self.assertEqual(exc.explanation, 'Resource not found')

    def test_ctor_with_empty_body(self):
        cls = self._getTargetSubclass(empty_body=True)
        exc = cls()
        self.assertEqual(exc.content_type, None)
        self.assertEqual(exc.content_length, None)

    def test_ctor_with_non_empty_body(self):
        cls = self._getTargetSubclass(empty_body=False)
        exc = cls()
        self.assertIsNotNone(exc.content_type)
        self.assertIsNotNone(exc.content_length)

    def test_ctor_with_invalid_code(self):
        with self.assertRaises(ValueError):
            cls = self._getTargetSubclass(code='invalid')
            exc = cls()