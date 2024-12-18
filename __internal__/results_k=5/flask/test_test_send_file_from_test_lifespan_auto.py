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
    assert not called  # Ensure called is initially empty
    instance.close()
    assert called == [42]  # Check if close method was called correctly

def test_close_method_already_called(app):
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)

    instance = TestClass()
    instance.close()
    assert called == [42]  # First call should append 42
    instance.close()  # Call again
    assert called == [42, 42]  # Check if close method can be called multiple times