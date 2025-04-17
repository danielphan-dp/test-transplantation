import unittest
from pyramid.urldispatch import _compile_route
from pyramid.util import text_

class TestCompileRouteFunctional(unittest.TestCase):
    def generates(self, pattern, dict, result):
        self.assertEqual(_compile_route(pattern)[1](dict), result)

    def test_generator_functional_edge_cases(self):
        self.generates('/{x}', {'x': None}, '/None')
        self.generates('/{x}', {'x': ' '}, '/ ')
        self.generates('/{x}', {'x': '1234567890'}, '/1234567890')
        self.generates('/{x}', {'x': 'special!@#$%^&*()'}, '/special!@#$%^&*()')
        self.generates('/{x}', {'x': 'a/b/c/d/e'}, '/a/b/c/d/e')
        self.generates('/{x}', {'x': 'a?b=c'}, '/a?b=c')
        self.generates('/{x}', {'x': 'a#fragment'}, '/a#fragment')
        self.generates('/{x}', {'x': text_(b'\xe9\x9b\x85')}, '/\xe9\x9b\x85')
        self.generates('/foo/{id}', {'id': ''}, '/foo/')
        self.generates('/foo/{id}', {'id': 'bar/baz'}, '/foo/bar/baz')
        self.generates('/foo/{id}', {'id': text_(b'\xe9\x9b\x85')}, '/foo/\xe9\x9b\x85')