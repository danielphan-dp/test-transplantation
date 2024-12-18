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
    
    test_instance.closed = True
    assert test_instance.closed is True

def test_close_method_already_closed(client):
    called = []
    
    class TestClose:
        def close(self):
            called.append(42)
            self.closed = True

    test_instance = TestClose()
    test_instance.close()
    assert test_instance.closed is True
    
    with pytest.raises(AttributeError):
        test_instance.close()  # Attempting to close again should raise an error or be a no-op

def test_close_method_no_call(client):
    called = []
    
    class TestClose:
        def close(self):
            called.append(42)

    test_instance = TestClose()
    assert not hasattr(test_instance, 'closed')
    
    assert called == []  # Ensure close hasn't been called yet
    test_instance.close()
    assert called == [42]  # Ensure close was called once

def test_close_method_multiple_calls(client):
    called = []
    
    class TestClose:
        def close(self):
            called.append(42)

    test_instance = TestClose()
    test_instance.close()
    test_instance.close()  # Call close multiple times
    assert called == [42, 42]  # Ensure close was called twice