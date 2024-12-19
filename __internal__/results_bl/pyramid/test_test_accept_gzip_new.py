import os
import unittest

class TestAssertBody(unittest.TestCase):

    def test_assert_body_equal(self):
        body = b'Test content'
        filename = os.path.join('fixtures', 'test_file.txt')
        with open(filename, 'wb') as f:
            f.write(body)
        _assertBody(body, filename)

    def test_assert_body_not_equal(self):
        body = b'Test content'
        filename = os.path.join('fixtures', 'test_file.txt')
        with open(filename, 'wb') as f:
            f.write(b'Other content')
        with self.assertRaises(AssertionError):
            _assertBody(body, filename)

    def test_assert_body_with_newlines(self):
        body = b'Test\r\ncontent'
        filename = os.path.join('fixtures', 'test_file.txt')
        with open(filename, 'wb') as f:
            f.write(b'Test\ncontent')
        _assertBody(body, filename)

    def test_assert_body_with_empty_file(self):
        body = b'Test content'
        filename = os.path.join('fixtures', 'empty_file.txt')
        with open(filename, 'wb') as f:
            f.write(b'')
        with self.assertRaises(AssertionError):
            _assertBody(body, filename)

    def test_assert_body_with_nonexistent_file(self):
        body = b'Test content'
        filename = os.path.join('fixtures', 'nonexistent_file.txt')
        with self.assertRaises(FileNotFoundError):
            _assertBody(body, filename)