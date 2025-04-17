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
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)

    instance = TestClass()
    instance.close()
    instance.close()  # Call it again
    assert called.count(42) == 2

def test_close_method_no_call(app):
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)

    instance = TestClass()
    assert not called  # Ensure close hasn't been called
    instance.close()
    assert called  # Now it should be called

def test_close_method_with_context(app):
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)

    with app.app_context():
        instance = TestClass()
        instance.close()
        assert 42 in called

def test_close_method_multiple_instances(app):
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)

    instance1 = TestClass()
    instance2 = TestClass()
    instance1.close()
    instance2.close()
    assert called == [42, 42]  # Both instances should call close