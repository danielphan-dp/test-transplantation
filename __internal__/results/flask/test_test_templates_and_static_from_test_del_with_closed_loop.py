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

    test_instance = TestClass()
    test_instance.close()
    
    assert called == [42]

def test_close_method_multiple_calls(client):
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)

    test_instance = TestClass()
    test_instance.close()
    test_instance.close()
    
    assert called == [42, 42]

def test_close_method_no_calls(client):
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)

    test_instance = TestClass()
    
    assert called == []