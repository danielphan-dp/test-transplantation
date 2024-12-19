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
        cls = self._getTargetSubclass(code=code, title=title, explanation=explanation)
        exc = cls()
        self.assertEqual(exc.code, code)
        self.assertEqual(exc.title, title)
        self.assertEqual(exc.explanation, explanation)

    def test_get_target_subclass_with_empty_body(self):
        cls = self._getTargetSubclass(empty_body=True)
        exc = cls()
        self.assertTrue(exc.empty_body)

    def test_get_target_subclass_inherits_from_target_class(self):
        cls = self._getTargetSubclass()
        self.assertTrue(issubclass(cls, self._getTargetClass()))

    def test_get_target_subclass_creates_unique_instances(self):
        cls = self._getTargetSubclass()
        exc1 = cls()
        exc2 = cls()
        self.assertIsNot(exc1, exc2)

    def test_get_target_subclass_with_invalid_code(self):
        with self.assertRaises(ValueError):
            self._getTargetSubclass(code='invalid_code')