import unittest
from pyramid.util.text_ import text_
from pyramid.httpexceptions import HTTPException

class TestGetTargetSubclass(unittest.TestCase):

    def setUp(self):
        self.cls = self._getTargetSubclass()

    def test_default_values(self):
        subclass = self.cls()
        self.assertEqual(subclass.code, '200')
        self.assertEqual(subclass.title, 'OK')
        self.assertEqual(subclass.explanation, 'explanation')
        self.assertFalse(subclass.empty_body)

    def test_custom_values(self):
        subclass = self.cls(code='404', title='Not Found', explanation='Resource not found', empty_body=True)
        self.assertEqual(subclass.code, '404')
        self.assertEqual(subclass.title, 'Not Found')
        self.assertEqual(subclass.explanation, 'Resource not found')
        self.assertTrue(subclass.empty_body)

    def test_empty_body(self):
        subclass = self.cls(empty_body=True)
        environ = _makeEnviron()
        exc = subclass(body_template='${body}')
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertEqual(body, b'200 OK\n\n')

    def test_unicode_body_template(self):
        la = text_(b'/La Pe\xc3\xb1a', 'utf-8')
        subclass = self.cls()
        environ = _makeEnviron(unicodeval=la)
        exc = subclass(body_template='${unicodeval}')
        start_response = DummyStartResponse()
        body = list(exc(environ, start_response))[0]
        self.assertEqual(body, b'200 OK\n\n/La Pe\xc3\xb1a')

    def test_invalid_code(self):
        with self.assertRaises(HTTPException):
            subclass = self.cls(code='invalid_code')

    def test_no_title(self):
        subclass = self.cls(title='')
        self.assertEqual(subclass.title, '')

    def test_explanation_none(self):
        subclass = self.cls(explanation=None)
        self.assertIsNone(subclass.explanation)