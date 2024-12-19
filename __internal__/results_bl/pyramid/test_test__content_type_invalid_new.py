import unittest
from pyramid.httpexceptions import HTTPException

class TestGetTargetSubclass(unittest.TestCase):

    def test_get_target_subclass_default_values(self):
        cls = self._getTargetSubclass()
        instance = cls()
        self.assertEqual(instance.code, '200')
        self.assertEqual(instance.title, 'OK')
        self.assertEqual(instance.explanation, 'explanation')
        self.assertFalse(instance.empty_body)

    def test_get_target_subclass_custom_values(self):
        code = '404'
        title = 'Not Found'
        explanation = 'The requested resource was not found.'
        empty_body = True
        cls = self._getTargetSubclass(code, title, explanation, empty_body)
        instance = cls()
        self.assertEqual(instance.code, code)
        self.assertEqual(instance.title, title)
        self.assertEqual(instance.explanation, explanation)
        self.assertTrue(instance.empty_body)

    def test_get_target_subclass_empty_body(self):
        cls = self._getTargetSubclass(empty_body=True)
        instance = cls()
        self.assertTrue(instance.empty_body)

    def test_get_target_subclass_invalid_code(self):
        with self.assertRaises(HTTPException):
            cls = self._getTargetSubclass(code='invalid_code')
            instance = cls()