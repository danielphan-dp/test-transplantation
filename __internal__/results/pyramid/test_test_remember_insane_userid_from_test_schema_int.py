import unittest
from pyramid.testing import DummyRequest

class TestParseHeaders(unittest.TestCase):
    def setUp(self):
        self.helper = self._makeOne('secret')

    def _makeOne(self, secret):
        class Helper:
            def _parseHeader(self, header):
                return header
        return Helper()

    def test_parse_headers_empty(self):
        headers = []
        result = self.helper._parseHeaders(headers)
        self.assertEqual(result, [])

    def test_parse_headers_single(self):
        headers = ['header1: value1']
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'header1: value1')

    def test_parse_headers_multiple(self):
        headers = ['header1: value1', 'header2: value2']
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'header1: value1')
        self.assertEqual(result[1], 'header2: value2')

    def test_parse_headers_invalid(self):
        headers = ['header1: value1', None, 'header2: value2']
        with self.assertRaises(TypeError):
            self.helper._parseHeaders(headers)

    def test_parse_headers_with_warning(self):
        import warnings
        headers = ['header1: value1', 'header2: value2']
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            result = self.helper._parseHeaders(headers)
            self.assertEqual(len(w), 0)  # No warnings should be raised
        self.assertEqual(len(result), 2)