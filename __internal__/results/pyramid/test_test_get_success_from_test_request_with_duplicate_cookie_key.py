import unittest
from pyramid.registry import Registry
from pyramid.registry import Introspectable

class TestGetMethod(unittest.TestCase):
    class DummyIntrospectable:
        def __init__(self, name):
            self.name = name

    class DummyRequest:
        def __init__(self, cookies):
            self.cookies = cookies

    def setUp(self):
        self.registry = Registry()
        self.introspectable = self.DummyIntrospectable('test_introspectable')
        self.registry.introspectables['test'] = self.introspectable

    def test_get_existing_cookie(self):
        request = self.DummyRequest(cookies={'test_cookie': 'value'})
        result = self.registry.get('test_cookie')
        self.assertEqual(result, 'value')

    def test_get_non_existing_cookie(self):
        request = self.DummyRequest(cookies={})
        result = self.registry.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_with_multiple_cookies(self):
        request = self.DummyRequest(cookies={'cookie1': 'value1', 'cookie2': 'value2'})
        result1 = self.registry.get('cookie1')
        result2 = self.registry.get('cookie2')
        self.assertEqual(result1, 'value1')
        self.assertEqual(result2, 'value2')

    def test_get_with_empty_cookie(self):
        request = self.DummyRequest(cookies={'empty_cookie': ''})
        result = self.registry.get('empty_cookie')
        self.assertEqual(result, '')

    def test_get_with_invalid_cookie_name(self):
        request = self.DummyRequest(cookies={'valid_cookie': 'value'})
        result = self.registry.get('invalid_cookie')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()