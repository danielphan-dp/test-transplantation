import unittest
from pyramid.httpexceptions import HTTPException

class TestGetTargetSubclass(unittest.TestCase):

    def test_ctor_with_empty_body(self):
        cls = self._getTargetSubclass(empty_body=True)
        exc = cls('detail')
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertEqual(body, b'200 OK\n\nexplanation\n\n\n\n')

    def test_ctor_with_custom_code(self):
        cls = self._getTargetSubclass(code='404', title='Not Found')
        exc = cls('detail')
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertEqual(body, b'404 Not Found\n\nexplanation\n\n\ndetail\n\n')

    def test_ctor_with_custom_title(self):
        cls = self._getTargetSubclass(title='Custom Title')
        exc = cls('detail')
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertIn(b'Custom Title', body)

    def test_ctor_with_custom_explanation(self):
        cls = self._getTargetSubclass(explanation='Custom Explanation')
        exc = cls('detail')
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertIn(b'Custom Explanation', body)

    def test_ctor_with_invalid_code(self):
        with self.assertRaises(HTTPException):
            cls = self._getTargetSubclass(code='invalid_code')