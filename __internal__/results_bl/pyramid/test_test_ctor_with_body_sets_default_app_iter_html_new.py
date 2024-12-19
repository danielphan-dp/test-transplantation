import unittest
from pyramid.httpexceptions import HTTPException

class TestGetTargetSubclass(unittest.TestCase):

    def test_ctor_with_empty_body(self):
        cls = self._getTargetSubclass(empty_body=True)
        exc = cls('detail')
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertEqual(body, b'')  # Expecting empty body

    def test_ctor_with_custom_code(self):
        custom_code = '404'
        cls = self._getTargetSubclass(code=custom_code)
        exc = cls('detail')
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertTrue(b'404 Not Found' in body)

    def test_ctor_with_custom_title(self):
        custom_title = 'Not Found'
        cls = self._getTargetSubclass(title=custom_title)
        exc = cls('detail')
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertTrue(custom_title.encode() in body)

    def test_ctor_with_custom_explanation(self):
        custom_explanation = 'This is a custom explanation.'
        cls = self._getTargetSubclass(explanation=custom_explanation)
        exc = cls('detail')
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertTrue(custom_explanation.encode() in body)

    def test_ctor_with_invalid_code(self):
        with self.assertRaises(ValueError):
            cls = self._getTargetSubclass(code='invalid_code')

    def test_ctor_with_missing_title(self):
        cls = self._getTargetSubclass(title=None)
        exc = cls('detail')
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertNotIn(b'None', body)  # Ensure 'None' is not in the body

    def test_ctor_with_empty_title(self):
        cls = self._getTargetSubclass(title='')
        exc = cls('detail')
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertNotIn(b'', body)  # Ensure empty title does not appear

    def test_ctor_with_empty_explanation(self):
        cls = self._getTargetSubclass(explanation='')
        exc = cls('detail')
        environ = _makeEnviron()
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertNotIn(b'', body)  # Ensure empty explanation does not appear