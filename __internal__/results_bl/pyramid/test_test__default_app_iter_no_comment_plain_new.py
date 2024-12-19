import unittest
from pyramid.httpexceptions import HTTPException

class TestGetTargetSubclass(unittest.TestCase):

    def test_get_target_subclass_with_custom_code(self):
        cls = self._getTargetSubclass(code='404', title='Not Found', explanation='Resource not found')
        exc = cls()
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertEqual(start_response.headerlist[0][1], 'text/plain; charset=UTF-8')
        self.assertEqual(body, b'404 Not Found\n\nResource not found\n\n\n\n\n')

    def test_get_target_subclass_with_empty_body(self):
        cls = self._getTargetSubclass(empty_body=True)
        exc = cls()
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertEqual(start_response.headerlist[0][1], 'text/plain; charset=UTF-8')
        self.assertEqual(body, b'200 OK\n\nexplanation\n\n')

    def test_get_target_subclass_with_different_title(self):
        cls = self._getTargetSubclass(title='Custom Title')
        exc = cls()
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertEqual(start_response.headerlist[0][1], 'text/plain; charset=UTF-8')
        self.assertEqual(body, b'200 OK\n\nexplanation\n\n\n\n\n')

    def test_get_target_subclass_with_no_explanation(self):
        cls = self._getTargetSubclass(explanation='')
        exc = cls()
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertEqual(start_response.headerlist[0][1], 'text/plain; charset=UTF-8')
        self.assertEqual(body, b'200 OK\n\n\n\n\n\n\n')

    def test_get_target_subclass_with_invalid_code(self):
        with self.assertRaises(HTTPException):
            cls = self._getTargetSubclass(code='invalid_code')
            exc = cls()
            environ = _makeEnviron()
            start_response = DummyStartResponse()
            list(exc(environ, start_response))