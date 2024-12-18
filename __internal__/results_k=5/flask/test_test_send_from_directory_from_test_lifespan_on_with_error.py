import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

def test_close_method(app):
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)

    instance = TestClass()
    instance.close()
    assert 42 in called

def test_close_method_already_called(app):
    called = [42]
    
    class TestClass:
        def close(self):
            called.append(42)

    instance = TestClass()
    instance.close()
    assert called.count(42) == 2

def test_close_method_no_call(app):
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)

    instance = TestClass()
    assert not called
    instance.close()
    assert called == [42]