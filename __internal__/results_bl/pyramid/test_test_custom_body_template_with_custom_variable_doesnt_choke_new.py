import unittest
from pyramid.httpexceptions import HTTPException

class TestGetTargetSubclass(unittest.TestCase):

    def test_default_subclass_properties(self):
        cls = self._getTargetSubclass()
        instance = cls()
        self.assertEqual(instance.code, '200')
        self.assertEqual(instance.title, 'OK')
        self.assertEqual(instance.explanation, 'explanation')
        self.assertFalse(instance.empty_body)

    def test_custom_code(self):
        cls = self._getTargetSubclass(code='404')
        instance = cls()
        self.assertEqual(instance.code, '404')

    def test_custom_title(self):
        cls = self._getTargetSubclass(title='Not Found')
        instance = cls()
        self.assertEqual(instance.title, 'Not Found')

    def test_custom_explanation(self):
        cls = self._getTargetSubclass(explanation='Resource not found')
        instance = cls()
        self.assertEqual(instance.explanation, 'Resource not found')

    def test_empty_body_true(self):
        cls = self._getTargetSubclass(empty_body=True)
        instance = cls()
        self.assertTrue(instance.empty_body)

    def test_empty_body_false(self):
        cls = self._getTargetSubclass(empty_body=False)
        instance = cls()
        self.assertFalse(instance.empty_body)

    def test_subclass_inheritance(self):
        cls = self._getTargetSubclass()
        subclass = cls()
        self.assertIsInstance(subclass, cls)

    def test_exception_handling_in_subclass(self):
        cls = self._getTargetSubclass()
        with self.assertRaises(HTTPException):
            raise cls()  # Simulating an exception being raised from the subclass

    def test_custom_body_template_with_invalid_variable(self):
        cls = self._getTargetSubclass()
        exc = cls(body_template='${INVALID_VARIABLE}')
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertNotIn(b'INVALID_VARIABLE', body)  # Ensure invalid variable is not in the response

    def test_subclass_with_no_arguments(self):
        cls = self._getTargetSubclass()
        instance = cls()
        self.assertEqual(instance.code, '200')
        self.assertEqual(instance.title, 'OK')
        self.assertEqual(instance.explanation, 'explanation')
        self.assertFalse(instance.empty_body)