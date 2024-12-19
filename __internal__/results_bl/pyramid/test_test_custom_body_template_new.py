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

    def test_custom_code(self):
        cls = self._getTargetSubclass(code='404')
        exc = cls()
        self.assertEqual(exc.code, '404')

    def test_custom_title(self):
        cls = self._getTargetSubclass(title='Not Found')
        exc = cls()
        self.assertEqual(exc.title, 'Not Found')

    def test_custom_explanation(self):
        cls = self._getTargetSubclass(explanation='Resource not found')
        exc = cls()
        self.assertEqual(exc.explanation, 'Resource not found')

    def test_empty_body(self):
        cls = self._getTargetSubclass(empty_body=True)
        exc = cls()
        self.assertTrue(exc.empty_body)

    def test_custom_body_template_with_empty_body(self):
        cls = self._getTargetSubclass(empty_body=True)
        exc = cls(body_template='${REQUEST_METHOD}')
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertEqual(body, b'200 OK\n\n')

    def test_invalid_code(self):
        with self.assertRaises(ValueError):
            cls = self._getTargetSubclass(code='invalid')
            exc = cls()