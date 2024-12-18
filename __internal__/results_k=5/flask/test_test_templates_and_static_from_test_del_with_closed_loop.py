import pytest
from blueprintapp import app

@pytest.fixture
def client():
    return app.test_client()

def test_close_method(client):
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)

    instance = TestClass()
    instance.close()
    
    assert called == [42]

def test_close_method_multiple_calls(client):
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)

    instance = TestClass()
    instance.close()
    instance.close()
    
    assert called == [42, 42]

def test_close_method_no_call(client):
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)

    instance = TestClass()
    
    assert called == []  # Ensure close was not called

def test_close_method_with_context(client):
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)

    instance = TestClass()
    with app.app_context():
        instance.close()
    
    assert called == [42]