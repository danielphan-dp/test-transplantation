import pytest
from gluon.example_main import foo


def test_foo():
    assert foo() == 2
    pass
