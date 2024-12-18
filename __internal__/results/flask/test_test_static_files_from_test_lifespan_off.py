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
    assert called == [42]

def test_close_method_multiple_calls(app):
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)

    instance = TestClass()
    instance.close()
    instance.close()
    assert called == [42, 42]

def test_close_method_no_call(app):
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)

    instance = TestClass()
    assert called == []  # Ensure close hasn't been called yet

def test_close_method_with_context(app):
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)

    with app.app_context():
        instance = TestClass()
        instance.close()
        assert called == [42]