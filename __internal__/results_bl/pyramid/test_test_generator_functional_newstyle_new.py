import unittest
from pyramid.util import text_
from pyramid.urldispatch import _compile_route

class TestURLDispatch(unittest.TestCase):

    def generates(self, pattern, dict, result):
        self.assertEqual(_compile_route(pattern)[1](dict), result)

    def test_generator_functional_edge_cases(self):
        self.generates('/{x}', {'x': None}, '/None')
        self.generates('/{x}', {'x': ' '}, '/ ')
        self.generates('/{x}', {'x': '123'}, '/123')
        self.generates('/{x}', {'x': 'special!@#'}, '/special!@#')
        self.generates('/{x}', {'x': 'a/b/c/d/e'}, '/a/b/c/d/e')
        self.generates('/{x}', {'x': 'a?b=c'}, '/a?b=c')
        self.generates('/{x}', {'x': 'a#fragment'}, '/a#fragment')
        self.generates('/{x}', {'x': 'a/b/c?query=1'}, '/a/b/c?query=1')
        self.generates('/{x}', {'x': text_(b'\xe9'), 'y': 'extra'}, '/%C3%A9')
        self.generates('/foo/{id}', {'id': ''}, '/foo/')
        self.generates('/foo/{id}', {'id': '0'}, '/foo/0')
        self.generates('/foo/{id}', {'id': '1.5'}, '/foo/1.5')
        self.generates('/foo/{id}', {'id': 'bar/baz'}, '/foo/bar/baz')
        self.generates('/foo/{id}', {'id': 'a/b/c/d/e/f/g/h/i/j/k/l/m/n/o/p/q/r/s/t/u/v/w/x/y/z'}, '/foo/a/b/c/d/e/f/g/h/i/j/k/l/m/n/o/p/q/r/s/t/u/v/w/x/y/z')