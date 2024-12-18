import unittest
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):
    def setUp(self):
        self.policy = self._makeOne(None)

    def test_call_with_non_empty_pathinfo(self):
        environ = self._getEnviron(key='value')
        request = DummyRequest(environ, path_info='/some/path')
        result = self.policy(request)
        self.assertEqual(result['context'], None)
        self.assertEqual(result['view_name'], '')
        self.assertEqual(result['subpath'], ())
        self.assertEqual(result['traversed'], ())
        self.assertEqual(result['root'], self.policy.root)
        self.assertEqual(result['virtual_root'], self.policy.root)
        self.assertEqual(result['virtual_root_path'], ())

    def test_call_with_multiple_keys(self):
        environ = self._getEnviron(key1='value1', key2='value2')
        request = DummyRequest(environ, path_info='/another/path')
        result = self.policy(request)
        self.assertEqual(result['context'], None)
        self.assertEqual(result['view_name'], '')
        self.assertEqual(result['subpath'], ())
        self.assertEqual(result['traversed'], ())
        self.assertEqual(result['root'], self.policy.root)
        self.assertEqual(result['virtual_root'], self.policy.root)
        self.assertEqual(result['virtual_root_path'], ())

    def test_call_with_none_key(self):
        environ = self._getEnviron(key=None)
        request = DummyRequest(environ, path_info='/none/key')
        result = self.policy(request)
        self.assertEqual(result['context'], None)
        self.assertEqual(result['view_name'], '')
        self.assertEqual(result['subpath'], ())
        self.assertEqual(result['traversed'], ())
        self.assertEqual(result['root'], self.policy.root)
        self.assertEqual(result['virtual_root'], self.policy.root)
        self.assertEqual(result['virtual_root_path'], ())

    def test_call_with_empty_environ(self):
        environ = self._getEnviron()
        request = DummyRequest(environ, path_info='/empty/environ')
        result = self.policy(request)
        self.assertEqual(result['context'], None)
        self.assertEqual(result['view_name'], '')
        self.assertEqual(result['subpath'], ())
        self.assertEqual(result['traversed'], ())
        self.assertEqual(result['root'], self.policy.root)
        self.assertEqual(result['virtual_root'], self.policy.root)
        self.assertEqual(result['virtual_root_path'], ())

    def _makeOne(self, *args, **kwargs):
        # Mock implementation of the method to create the policy object
        return lambda request: {
            'context': None,
            'view_name': '',
            'subpath': (),
            'traversed': (),
            'root': self,
            'virtual_root': self,
            'virtual_root_path': ()
        }

    def _getEnviron(self, **kw):
        environ = {}
        environ.update(kw)
        return environ

if __name__ == '__main__':
    unittest.main()