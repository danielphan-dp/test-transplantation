import unittest
from pyramid.urldispatch import _compile_route
from pyramid.util import text_

class TestCompileRouteFunctional(unittest.TestCase):
    def generates(self, pattern, dict, result):
        self.assertEqual(_compile_route(pattern)[1](dict), result)

    def test_empty_pattern(self):
        self.generates('', {}, '')

    def test_pattern_with_special_characters(self):
        self.generates('/foo/{x}', {'x': '!', '/': '%2F'}, '/foo/!')

    def test_pattern_with_multiple_parameters(self):
        self.generates('/foo/{x}/{y}', {'x': 'bar', 'y': 'baz'}, '/foo/bar/baz')

    def test_pattern_with_encoded_characters(self):
        self.generates('/foo/{x}', {'x': text_(b'/La Pe\xc3\xb1a', 'utf-8')}, '/foo//La%20Pe%C3%B1a')

    def test_pattern_with_trailing_slash(self):
        self.generates('/foo/{x}/', {'x': 'bar'}, '/foo/bar/')

    def test_pattern_with_query_parameters(self):
        self.generates('/foo/{x}', {'x': 'bar?query=1'}, '/foo/bar%3Fquery%3D1')

    def test_pattern_with_empty_dict(self):
        self.generates('/foo', {}, '/foo')

    def test_pattern_with_nested_traversal(self):
        self.generates('/foo/{x}*traverse', {'x': 'bar', 'traverse': '/baz/qux'}, '/foo/bar/baz/qux')

    def test_pattern_with_non_string_dict(self):
        self.generates('/foo/{x}', {'x': 123}, '/foo/123')

    def test_pattern_with_multiple_traversals(self):
        self.generates('/foo/{x}*traverse1/{y}*traverse2', {'x': 'bar', 'traverse1': '/baz', 'y': 'qux', 'traverse2': '/quux'}, '/foo/bar/baz/qux/quux')