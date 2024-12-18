import pytest
from flask import Flask
from blueprintapp import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_close_method(client):
    called = []
    
    class TestClose:
        def close(self):
            called.append(42)

    test_instance = TestClose()
    assert not hasattr(test_instance, 'closed')
    
    test_instance.close()
    assert called == [42]
    
    # Simulate closing the app context
    test_instance.closed = True
    assert test_instance.closed is True

def test_close_method_already_closed(client):
    called = []
    
    class TestClose:
        def close(self):
            called.append(42)

    test_instance = TestClose()
    test_instance.closed = True
    
    with pytest.raises(AttributeError):
        test_instance.close()  # Should not allow closing again

def test_close_method_no_call(client):
    called = []
    
    class TestClose:
        def close(self):
            called.append(42)

    test_instance = TestClose()
    assert called == []
    assert not hasattr(test_instance, 'closed')