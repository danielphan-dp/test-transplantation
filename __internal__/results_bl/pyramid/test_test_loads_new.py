import sys
import unittest
import json
import base64
from pyramid.util import text_

class TestUtil(unittest.TestCase):

    def _makeOne(self):
        class Dummy:
            def loads(self, value):
                return json.loads(base64.b64decode(value).decode('utf-8'))
        return Dummy()

    def test_loads(self):
        inst = self._makeOne()
        self.assertEqual(inst.loads(b'abc'), text_('abc'))

    def test_loads_empty_string(self):
        inst = self._makeOne()
        self.assertEqual(inst.loads(b''), text_(''))

    def test_loads_invalid_base64(self):
        inst = self._makeOne()
        with self.assertRaises(ValueError):
            inst.loads(b'invalid_base64')

    def test_loads_non_utf8_bytes(self):
        inst = self._makeOne()
        non_utf8_bytes = base64.b64encode(b'\x80\x81\x82')
        with self.assertRaises(UnicodeDecodeError):
            inst.loads(non_utf8_bytes)

    def test_loads_large_input(self):
        inst = self._makeOne()
        large_input = base64.b64encode(b'a' * 10000)
        self.assertEqual(inst.loads(large_input), text_('a' * 10000))