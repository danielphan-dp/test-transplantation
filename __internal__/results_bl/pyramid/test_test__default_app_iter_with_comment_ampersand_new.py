import unittest
from pyramid.httpexceptions import HTTPException

class TestGetTargetSubclass(unittest.TestCase):

    def test_default_app_iter_with_empty_body(self):
        cls = self._getTargetSubclass(empty_body=True)
        exc = cls()
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))
        self.assertEqual(len(body), 0)

    def test_default_app_iter_with_custom_code(self):
        custom_code = '404'
        cls = self._getTargetSubclass(code=custom_code)
        exc = cls()
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        for header in start_response.headerlist:
            if header[0] == 'Status':
                self.assertEqual(header[1], custom_code)

    def test_default_app_iter_with_custom_title(self):
        custom_title = 'Not Found'
        cls = self._getTargetSubclass(title=custom_title)
        exc = cls()
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertIn(custom_title.encode(), body)

    def test_default_app_iter_with_custom_explanation(self):
        custom_explanation = 'The requested resource was not found.'
        cls = self._getTargetSubclass(explanation=custom_explanation)
        exc = cls()
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertIn(custom_explanation.encode(), body)

    def test_default_app_iter_with_invalid_code(self):
        with self.assertRaises(HTTPException):
            cls = self._getTargetSubclass(code='invalid')
            exc = cls()
            environ = _makeEnviron()
            start_response = DummyStartResponse()
            list(exc(environ, start_response))