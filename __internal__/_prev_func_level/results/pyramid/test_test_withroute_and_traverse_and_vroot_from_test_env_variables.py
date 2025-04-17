import unittest
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):

    def test_get_environ_with_single_key_value(self):
        result = self._getEnviron(HTTP_X_VHM_ROOT='/abc')
        self.assertEqual(result, {'HTTP_X_VHM_ROOT': '/abc'})

    def test_get_environ_with_multiple_key_values(self):
        result = self._getEnviron(HTTP_X_VHM_ROOT='/abc', SERVER_NAME='example.com', SERVER_PORT='80')
        self.assertEqual(result, {'HTTP_X_VHM_ROOT': '/abc', 'SERVER_NAME': 'example.com', 'SERVER_PORT': '80'})

    def test_get_environ_with_empty(self):
        result = self._getEnviron()
        self.assertEqual(result, {})

    def test_get_environ_with_none_value(self):
        result = self._getEnviron(HTTP_X_VHM_ROOT=None)
        self.assertEqual(result, {'HTTP_X_VHM_ROOT': None})

    def test_get_environ_with_special_characters(self):
        result = self._getEnviron(HTTP_X_VHM_ROOT='path/with special&chars!')
        self.assertEqual(result, {'HTTP_X_VHM_ROOT': 'path/with special&chars!'})